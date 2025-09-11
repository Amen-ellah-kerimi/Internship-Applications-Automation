import imaplib
import email
from email.header import decode_header
import re
import os
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
    match = re.search(r'<(.+?)>', sender)
    return match.group(1) if match else sender

def extract_name(sender):
    match = re.match(r'(.*?)<', sender)
    return match.group(1).strip() if match else sender.split('@')[0]

def parse_candidate(body: str, sender: str):
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

def save_attachments(attachments, folder):
    os.makedirs(folder, exist_ok=True)
    saved_files = []
    for att_name, att_data in attachments:
        if att_name and att_data:
            file_path = os.path.join(folder, att_name)
            with open(file_path, 'wb') as f:
                f.write(att_data)
            saved_files.append(file_path)
    return saved_files

def fetch_and_save_emails(imap_server, email_user, email_pass, folder="INBOX", code_map=None, attachment_folder="attachements"):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        mail.select(folder)
    except Exception as e:
        raise RuntimeError(f"IMAP error: {e}")

    status, messages = mail.search(None, "UNSEEN")
    if status != "OK":
        raise RuntimeError("Failed to search mailbox.")

    candidates = []
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
                if code_map is None:
                    code_map = {}
                subject_match = re.match(r"Internship Application\s*[–-]\s*(\w+)\s*[–-]\s*(.+)", subject)
                if subject_match:
                    code = subject_match.group(1)
                    name_from_subject = subject_match.group(2).strip()
                    candidate_data["name"] = name_from_subject
                    candidate_data["internship"] = code_map.get(code, code)
                else:
                    code_match = re.search(r"Internship Application\s*[–-]\s*(\w+)", subject)
                    if code_match:
                        code = code_match.group(1)
                        candidate_data["internship"] = code_map.get(code, code)
                saved_files = save_attachments(attachments, attachment_folder)
                candidate_data["attachments"] = saved_files
                candidates.append(candidate_data)
                mail.store(msg_id, '+FLAGS','\\Seen')
    return candidates
