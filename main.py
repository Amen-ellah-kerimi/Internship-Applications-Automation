import os
from dotenv import load_dotenv
from email_client import validate_email_creds, connect_email, fetch_unread_emails, mark_email_read
from parser import parse_email
from candidate_extractor import extract_candidate_info
from csv_handler import append_candidate
from utils import timestamp_now

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"
CSV_PATH = "candidates.csv"

# Validate credentials
validate_email_creds(EMAIL_USER, EMAIL_PASS)

# Connect to mailbox
mail = connect_email(EMAIL_USER, EMAIL_PASS, IMAP_SERVER)

# Fetch unread internship emails
messages = fetch_unread_emails(mail)

for msg_id in messages:
    _, msg_data = mail.fetch(msg_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg_dict = parse_email(response_part[1])
            
            # Extract structured candidate info
            candidate = extract_candidate_info(msg_dict["body"])
            if candidate:
                # Add meta info
                candidate.update({
                    "subject": msg_dict["subject"],
                    "sender": msg_dict["sender"],
                    "received_date": timestamp_now(),
                    "notes": ""
                })
                append_candidate(CSV_PATH, candidate)
                print(f"Saved candidate: {candidate.get('name', 'Unknown')}")

            # Mark email as read
            mark_email_read(mail, msg_id)

