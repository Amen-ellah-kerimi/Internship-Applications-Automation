import imaplib
import email
from email.header import decode_header
import re
import os
import logging
from typing import List, Optional

class Attachment:
    """Represents an email attachment."""
    def __init__(self, filename: str, data: bytes):
        self.filename = filename
        self.data = data

class EmailMessage:
    """Represents a parsed email message."""
    def __init__(self, subject: str, sender: str, body: str, attachments: List[Attachment]):
        self.subject = subject
        self.sender = sender
        self.body = body
        self.attachments = attachments

class IMAPClient:
    """IMAP client for connecting, searching, and fetching emails."""
    def __init__(self, server: str, user: str, password: str, folder: str = "INBOX"):
        self.server = server
        self.user = user
        self.password = password
        self.folder = folder
        self.connection = None

    def connect(self):
        """Connect to the IMAP server and select the folder."""
        try:
            self.connection = imaplib.IMAP4_SSL(self.server)
            self.connection.login(self.user, self.password)
            self.connection.select(self.folder)
            logging.info(f"Connected to {self.server}, folder {self.folder}")
        except Exception as e:
            logging.error(f"IMAP connection failed: {e}")
            raise

    def search(self, criteria: str = "UNSEEN") -> List[bytes]:
        """Search for emails matching the criteria."""
        try:
            status, messages = self.connection.search(None, criteria)
            if status != "OK":
                logging.warning(f"Search failed: {status}")
                return []
            return messages[0].split()
        except Exception as e:
            logging.error(f"Search error: {e}")
            return []

    def fetch_email(self, msg_id: bytes) -> Optional[EmailMessage]:
        """Fetch and parse a single email by message ID."""
        try:
            _, msg_data = self.connection.fetch(msg_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = self._safe_decode(msg.get("Subject"))
                    sender = self._safe_decode(msg.get("From"))
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
                                attachments.append(Attachment(att_name, att_data))
                    else:
                        payload = msg.get_payload(decode=True)
                        if payload:
                            body = payload.decode(errors="ignore")
                    return EmailMessage(subject, sender, body, attachments)
            return None
        except Exception as e:
            logging.error(f"Failed to fetch email {msg_id}: {e}")
            return None

    def mark_read(self, msg_id: bytes):
        """Mark an email as read."""
        try:
            self.connection.store(msg_id, '+FLAGS','\\Seen')
        except Exception as e:
            logging.warning(f"Failed to mark email {msg_id} as read: {e}")

    def logout(self):
        """Logout from the IMAP server."""
        if self.connection:
            try:
                self.connection.logout()
                logging.info("Logged out from IMAP server.")
            except Exception as e:
                logging.warning(f"Logout failed: {e}")

    @staticmethod
    def _safe_decode(header_value):
        """Safely decode an email header value."""
        if not header_value:
            return ""
        decoded, encoding = decode_header(header_value)[0]
        if isinstance(decoded, bytes):
            return decoded.decode(encoding if encoding else "utf-8", errors="ignore")
        return decoded
