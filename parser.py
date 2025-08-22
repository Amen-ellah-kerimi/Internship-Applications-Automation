from email.header import decode_header
import email
import re

def safe_decode(header_value): 
    if not header_value:
        return ""
    decoded, encoding = decode_header(header_value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding if encoding else "utf-8", errors="ignore")
    return decoded

def parse_email(msg_bytes):
    msg = email.message_from_bytes(msg_bytes)

    subject = safe_decode(msg.get("Subject"))
    sender  = safe_decode(msg.get("From"))

    body = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disp = part.get("Content-Disposition")

            # Plain text body
            if content_type == "text/plain" and (not content_disp or "attachment" not in content_disp.lower()):
                payload = part.get_payload(decode=True)
                if isinstance(payload, bytes):
                    body = payload.decode(errors="ignore")
                

            # Attachments
            if content_disp and "attachment" in content_disp.lower():
                attachments.append(part)
    else:
        payload = msg.get_payload(decode=True)
        if isinstance(payload, bytes):
            body = payload.decode(errors="ignore")
    
    return {
        "subject": subject,
        "sender": sender,
        "body": body,
        "attachments": attachments
    }

def validate_subject(subject, code_map):
    pattern = r"^Internship Application - .+ - (\w+)$"
    match = re.match(pattern, subject.strip())
    if match:
        code = match.group(1)
        return code_map.get(code)  # returns internship type
    return None

