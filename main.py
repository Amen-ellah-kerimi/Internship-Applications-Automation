import os
from dotenv import load_dotenv
from email_client import validate_email_creds, connect_email, fetch_unread_emails, mark_email_read
from parser import parse_email, save_attachments
from candidate_extractor import extract_candidate_info
from csv_handler import append_candidate
from utils import timestamp_now
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"
CSV_PATH = "candidates.csv"

# NOTE: For production, you can run this script periodically using cron or systemd instead of the loop below.
# Example cron: */5 * * * * python /path/to/main.py


def process_inbox(mail):
    try:
        messages = fetch_unread_emails(mail)
        for msg_id in messages:
            _, msg_data = mail.fetch(msg_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    try:
                        msg_dict = parse_email(response_part[1])
                        attachment_paths = save_attachments(msg_dict["attachments"])
                        candidate = extract_candidate_info(msg_dict["body"], msg_dict["sender"])
                        if candidate:
                            candidate.update({
                                "subject": msg_dict["subject"],
                                "sender": msg_dict["sender"],
                                "received_date": timestamp_now(),
                                "notes": "",
                                "cv": attachment_paths[0] if attachment_paths else "N/A"
                            })
                            append_candidate(CSV_PATH, candidate)
                            logging.info(f"Saved candidate: {candidate.get('name', 'Unknown')}")
                        mark_email_read(mail, msg_id)
                    except Exception:
                        logging.exception("Error processing email message")
    except Exception:
        logging.exception("Error fetching emails from inbox")

def main_loop():
    while True:
        try:
            process_inbox(mail)
        except Exception:
            logging.exception("Error in main loop")
        time.sleep(300)  # Wait for 5 minutes before checking again

if __name__ == "__main__":
    # Validate credentials
    validate_email_creds(EMAIL_USER, EMAIL_PASS)
    # TODO: Add error handling for credential validation

    # Connect to mailbox
    mail = connect_email(EMAIL_USER, EMAIL_PASS, IMAP_SERVER)
    # TODO: Add error handling for mailbox connection

    main_loop()

