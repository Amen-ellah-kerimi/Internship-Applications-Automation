import imaplib
import os
from dotenv import load_dotenv

import email
from email.header import decode_header


# Loading env Variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"

# Validating env Variables

if EMAIL_USER is None or EMAIL_PASS is None:
    raise ValueError("EMAIL_USER or EMAIL_PASS not set in .env")


# Connect to the mailbox
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_USER,EMAIL_PASS)
mail.select("inbox")

status, messages = mail.search(None, '(UNSEEN SUBJECT "Internship")')
messages = messages[0].split()
print(f"Found {len(messages)} new internship emails.")


for msg_num in messages:
    status, msg_data = mail.fetch(msg_num, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part,tuple):
            msg = email.message_from_bytes(response_part[1])

            # Decode subject 
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            
            sender = msg.get("From")

            # Extract the body 
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
            else:
                body = msg.get_payload(decode=True).decode()

            print(f"From:  {sender}\nSubject: {subject}\nBody:\n{body}")

