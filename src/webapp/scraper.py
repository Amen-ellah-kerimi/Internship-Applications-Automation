import imaplib
import email
from email.header import decode_header
import re
from src.webapp.models import db, Candidate, Attachment
from src.webapp.app import app
from datetime import datetime, timezone

# ------------------ Helpers ------------------

def safe_decode(header_value):
    if not header_value:
        return ""
    decoded, encoding = decode_header(header_value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding if encoding else "utf-8", errors="ignore")
    return decoded

def extract_email(sender):
    import re
    match = re.search(r'<(.+?)>', sender)
    return match.group(1) if match else sender

def extract_name(sender):
    match = re.match(r'(.*?)<', sender)
    return match.group(1).strip() if match else sender.split('@')[0]

def parse_candidate(body: str, sender: str):
    """Extract candidate info from email body and sender"""
    name_match = re.search(r"Name[:\s]+(.+)", body, re.IGNORECASE)
    phone_match = re.search(r"Phone[:\s]+([+\d\s\-()]+)", body, re.IGNORECASE)
    linkedin_match = re.search(r"LinkedIn[:\s]+(https?://[\w\.-/]+|linkedin.com/in/[\w\-]+)", body, re.IGNORECASE)
    github_match = re.search(r"GitHub[:\s]+(https?://[\w\.-/]+|github.com/[\w\-]+)", body, re.IGNORECASE)
    internship_match = re.search(r"Internship[:\s]+([\w\s]+)", body, re.IGNORECASE)
    code_match = re.search(r"Internship Code[:\s]+(\w+)", body, re.IGNORECASE)

    email_addr = extract_email(sender)
    name = name_match.group(1).strip() if name_match else extract_name(sender)
    linkedin = linkedin_match.group(1).strip() if linkedin_match else None
    github = github_match.group(1).strip() if github_match else None
    phone = phone_match.group(1).strip() if phone_match else None
    internship = internship_match.group(1).strip() if internship_match else (code_match.group(1).strip() if code_match else None)

    return {
        "name": name,
        "email": email_addr,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "internship": internship,
        "notes": body
    }

def save_candidate(candidate_data, attachments):
    """Save candidate and attachments to DB, skip duplicates by email"""
    import os
    with app.app_context():
        existing = Candidate.query.filter_by(email=candidate_data["email"]).first()
        if existing:
            return existing, []
        candidate = Candidate(
            name=candidate_data["name"],
            email=candidate_data["email"],
            phone=candidate_data.get("phone"),
            linkedin=candidate_data.get("linkedin"),
            internship=candidate_data.get("internship"),
            notes=candidate_data.get("notes"),
            applied_on=datetime.now(timezone.utc)
        )
        db.session.add(candidate)
        db.session.commit()

        saved_attachments = []
        attachment_folder = '/home/amen/stage/career/attachements'
        os.makedirs(attachment_folder, exist_ok=True)
        for att_name, att_data in attachments:
            if att_name and att_data:
                file_path = os.path.join(attachment_folder, att_name)
                with open(file_path, 'wb') as f:
                    f.write(att_data)
                rel_path = os.path.relpath(file_path, os.path.dirname(__file__))
                att = Attachment(
                    candidate_id=candidate.id,
                    filename=att_name,
                    file_type=None,
                    path=rel_path,
                    uploaded_on=datetime.now(timezone.utc)
                )
                db.session.add(att)
                saved_attachments.append(att)
        db.session.commit()
        return candidate, saved_attachments

# ------------------ Core Scraper ------------------

def fetch_and_save_emails(imap_server, email_user, email_pass, folder="INBOX"):
    """
    Connect to IMAP, fetch unread emails, parse and save to DB.
    Returns dict: {"new_count": int} or {"error": str}
    """
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        mail.select(folder)
    except Exception as e:
        return {"error": str(e)}

    status, messages = mail.search(None, "UNSEEN")
    if status != "OK":
        return {"error": "Failed to search mailbox."}

    new_count = 0

    # Get internship code map from settings
    from src.webapp.models import Setting
    import json
    setting = Setting.query.first()
    code_map = {}
    if setting and getattr(setting, 'internship_code_map', None):
        try:
            code_map = json.loads(setting.internship_code_map)
        except Exception:
            code_map = {}

    for msg_id in messages[0].split():
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender = safe_decode(msg.get("From"))
                subject = safe_decode(msg.get("Subject"))
                body = ""
                attachments = []

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disp = part.get("Content-Disposition")
                        if content_type == "text/plain" and (not content_disp or "attachment" not in content_disp.lower()):
                            payload = part.get_payload(decode=True)
                            if payload:
                                body = payload.decode(errors="ignore")
                        if content_disp and "attachment" in content_disp.lower():
                            att_name = part.get_filename()
                            att_data = part.get_payload(decode=True)
                            attachments.append((att_name, att_data))
                else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                        body = payload.decode(errors="ignore")

                candidate_data = parse_candidate(body, sender)
                # Try to extract internship code and name from subject
                subject_match = re.match(r"Internship Application\s*[–-]\s*(\w+)\s*[–-]\s*(.+)", subject)
                if subject_match:
                    code = subject_match.group(1)
                    name_from_subject = subject_match.group(2).strip()
                    candidate_data["name"] = name_from_subject
                    candidate_data["internship"] = code_map.get(code, code)
                else:
                    # Fallback: code only
                    code_match = re.search(r"Internship Application\s*[–-]\s*(\w+)", subject)
                    if code_match:
                        code = code_match.group(1)
                        candidate_data["internship"] = code_map.get(code, code)
                candidate, saved_atts = save_candidate(candidate_data, attachments)
                # Only count if not duplicate
                if saved_atts or (candidate and getattr(candidate, 'id', None)):
                    new_count += 1
                mail.store(msg_id, '+FLAGS','\\Seen')

    return {"new_count": new_count}

