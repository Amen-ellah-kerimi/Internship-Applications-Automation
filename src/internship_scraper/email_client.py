
import imaplib
import logging
from typing import Optional, List, Any
from .config_loader import get_config

def validate_email_creds(user: Optional[str], password: Optional[str]) -> None:
    """
    Validate that email credentials are provided.

    Args:
        user (Optional[str]): Email username.
        password (Optional[str]): Email password.

    Returns:
        None

    Notes:
        - TODO: Add more robust credential validation (length, format).
        - FIXME: Credentials should be securely managed, not hardcoded.
    """
    if not user or not password:
        logging.error("EMAIL_USER or EMAIL_PASS not set.")
        raise ValueError("EMAIL_USER or EMAIL_PASS not set.")

def connect_email(
    user: Optional[str] = None,
    password: Optional[str] = None,
    server: Optional[str] = None,
    config_path: str = "defaults/email_config.yaml"
) -> Any:
    """
    Connect to the email server using credentials and server from config or arguments.

    Args:
        user (Optional[str]): Email username. If None, loads from config.
        password (Optional[str]): Email password. If None, loads from config.
        server (Optional[str]): IMAP server address. If None, loads from config.
        config_path (str): Path to email config YAML.

    Returns:
        Any: IMAP4_SSL connection object.

    Notes:
        - NOTE: Uses SSL for IMAP connection.
        - TODO: Support other folders and protocols.
        - FIXME: No retry logic for failed connections.
    """
    if not (user and password and server):
        config = get_config(config_path)
        user = user or config.get("email_user")
        password = password or config.get("email_pass")
        server = server or config.get("imap_server")
    validate_email_creds(user, password)
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(user, password)
        folder = config.get("email_folder", "inbox") if 'config' in locals() else "inbox"
        mail.select(folder)
        return mail
    except Exception:
        logging.exception("Error connecting to email server")
        raise

def fetch_unread_emails(mail: Any, folder: Optional[str] = None) -> List[bytes]:
    """
    Fetch unread email message IDs from the specified folder.

    Args:
        mail (Any): IMAP4_SSL connection object.
        folder (Optional[str]): Folder to search. If None, uses 'inbox'.

    Returns:
        List[bytes]: List of unread message IDs.

    Notes:
        - NOTE: Only fetches 'UNSEEN' emails.
        - TODO: Add support for batch size and polling interval from config.
        - FIXME: No error handling for folder selection failures.
    """
    try:
        if folder:
            mail.select(folder)
        _, messages = mail.search(None, 'UNSEEN')
        messages = messages[0].split()
        logging.info(f"Found {len(messages)} new internship emails")
        return messages
    except Exception:
        logging.exception("Error fetching unread emails")
        return []

def mark_email_read(mail: Any, msg_id: bytes) -> None:
    """
    Mark an email as read by its message ID.

    Args:
        mail (Any): IMAP4_SSL connection object.
        msg_id (bytes): Message ID to mark as read.

    Returns:
        None

    Notes:
        - TODO: Add error handling for invalid message IDs.
        - FIXME: No batch marking support.
    """
    try:
        mail.store(msg_id, '+FLAGS','\\Seen')
        logging.info(f"Marked email {msg_id} as read.")
    except Exception:
        logging.exception(f"Error marking email {msg_id} as read.")
