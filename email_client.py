import imaplib
import logging

def validate_email_creds(user, password):
    if user is None or password is None:
        logging.error("EMAIL_USER or EMAIL_PASS not set in .env")
        raise ValueError("EMAIL_USER or EMAIL_PASS not set in .env")

def connect_email(user, password, server):
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(user, password)
        mail.select("inbox")
        return mail
    except Exception:
        logging.exception("Error connecting to email server")
        raise

def fetch_unread_emails(mail):
    try:
        _, messages = mail.search(None, 'UNSEEN')
        messages = messages[0].split()
        logging.info(f"Found {len(messages)} new internship emails")
        return messages
    except Exception:
        logging.exception("Error fetching unread emails")
        return []

def mark_email_read(mail, msg_id):
    try:
        mail.store(msg_id, '+FLAGS','\\Seen')
        logging.info(f"Marked email {msg_id} as read.")
    except Exception:
        logging.exception(f"Error marking email {msg_id} as read.")
