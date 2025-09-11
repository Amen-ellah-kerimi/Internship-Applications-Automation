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

def parse_candidate(body: str, sender_email: str):
    """Extract candidate info from email body"""
    name_match = re.search(r"Name[:\s]+(.+)", body, re.IGNORECASE)
    phone_match = re.search(r"Phone[:\s]+(\+?\d+)", body, re.IGNORECASE)
    linkedin_match = re.search(r"(https?://www.linkedin.com/in/[^\s]+)", body, re.IGNORECASE)
    code_match = re.search(r"Internship Code[:\s]+(\w+)", body, re.IGNORECASE)

    return {
        "name": name_match.group(1).strip() if name_match else "N/A",
        "email": sender_email,
        "phone": phone_match.group(1).strip() if phone_match else None,
        "linkedin": linkedin_match.group(1).strip() if linkedin_match else None,
        "internship": code_match.group(1).strip() if code_match else None
    }

def save_candidate(candidate_data, attachments):
    """Save candidate and attachments to DB"""
    with app.app_context():
        candidate = Candidate(
            name=candidate_data["name"],
            email=candidate_data["email"],
            phone=candidate_data["phone"],
            linkedin=candidate_data.get("linkedin"),
            internship=candidate_data.get("internship"),
            applied_on=datetime.now(timezone.utc)
        )
        db.session.add(candidate)
        db.session.commit()

        saved_attachments = []
        for att_name, att_data in attachments:
            att = Attachment(
                candidate_id=candidate.id,
                filename=att_name,
                file_type=None,
                path="",  # optionally store path if you save to disk
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
    Returns a list of saved Candidate objects.
    """
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_user, email_pass)
    mail.select(folder)

    status, messages = mail.search(None, "UNSEEN")
    if status != "OK":
        return []

    saved_candidates = []

    for msg_id in messages[0].split():
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender = safe_decode(msg.get("From"))
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
                candidate, saved_atts = save_candidate(candidate_data, attachments)
                saved_candidates.append(candidate)
                mail.store(msg_id, '+FLAGS','\\Seen')

    return saved_candidates

