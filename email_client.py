import imaplib

def validate_email_creds(user, password):
    if user is None or password is None:
        raise ValueError("EMAIL_USER or EMAIL_PASS not set in .env")


def connect_email(user, password, server):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(user, password)
    mail.select("inbox")
    return mail

def fetch_unread_emails(mail):
    _, messages = mail.search(None, 'UNSEEN')
    messages = messages[0].split()

    print(f"Found {len(messages)} new internship emails")
    return messages

def mark_email_read(mail, msg_id):
   mail.store(msg_id, '+FLAGS','\\Seen')
