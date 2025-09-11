
from email.header import decode_header
import email
import re
import os
import logging
from typing import Any, Dict, List, Optional
from .config_loader import get_config

def safe_decode(header_value: Any) -> str:
    """
    Safely decode an email header value.

    Args:
        header_value (Any): The header value to decode.

    Returns:
        str: Decoded header string.

    Notes:
        - TODO: Handle multiple encoded fragments in header.
        - FIXME: Encoding detection may fail for rare cases.
    """
    if not header_value:
        return ""
    decoded, encoding = decode_header(header_value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding if encoding else "utf-8", errors="ignore")
    return decoded

def parse_email(msg_bytes: bytes) -> Dict[str, Any]:
    """
    Parse an email message from raw bytes.

    Args:
        msg_bytes (bytes): Raw email message bytes.

    Returns:
        Dict[str, Any]: Parsed email fields (subject, sender, body, attachments).

    Notes:
        - NOTE: Only extracts plain text body and attachments.
        - TODO: Add HTML body extraction and validation.
        - FIXME: Multipart parsing may miss nested parts.
    """
    try:
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
    except Exception:
        logging.exception("Error parsing email")
        return {"subject": "N/A", "sender": "N/A", "body": "N/A", "attachments": []}

def get_code_map(config_path: str = "defaults/rules.yaml") -> Dict[str, str]:
    """
    Get internship code mapping from config.

    Args:
        config_path (str): Path to rules config YAML.

    Returns:
        Dict[str, str]: Mapping of codes to internship types.

    Notes:
        - NOTE: Used for subject validation and candidate extraction.
        - TODO: Validate config structure and handle missing codes.
    """
    try:
        config = get_config(config_path)
        return config.get("internship_code_map", {})
    except Exception:
        logging.exception(f"Error loading code map from config: {config_path}")
        return {}

def validate_subject(subject: str, code_map: Optional[Dict[str, str]] = None) -> str:
    """
    Validate and extract internship type from email subject using code map.

    Args:
        subject (str): Email subject string.
        code_map (Optional[Dict[str, str]]): Mapping of codes to internship types. If None, loads from config.

    Returns:
        str: Internship type or "N/A" if not found.

    Notes:
        - FIXME: Validate subject format strictly before extracting code.
        - TODO: Implement robust error handling for malformed subjects.
    """
    if code_map is None:
        code_map = get_code_map()
    pattern = r"^Internship Application - .+ - (\w+)$"
    match = re.match(pattern, subject.strip())
    if match:
        code = match.group(1)
        return code_map.get(code, "N/A")
    return "N/A"

def save_attachments(
    attachments: List[Any],
    folder: Optional[str] = None,
    config_path: str = "defaults/email_config.yaml"
) -> List[str]:
    """
    Save email attachments to disk in the specified folder.

    Args:
        attachments (List[Any]): List of email attachment parts.
        folder (Optional[str]): Folder to save attachments. If None, loads from config.
        config_path (str): Path to email config YAML.

    Returns:
        List[str]: List of saved file paths.

    Notes:
        - NOTE: Creates folder if it does not exist.
        - TODO: Add max size check and file type validation from config.
        - FIXME: No duplicate filename handling.
    """
    if folder is None:
        config = get_config(config_path)
        folder = config.get("attachment_folder", "attachments")
    os.makedirs(folder, exist_ok=True)
    file_paths = []
    for part in attachments:
        filename = part.get_filename()
        if filename:
            filepath = os.path.join(folder, filename)
            try:
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                file_paths.append(filepath)
                logging.info(f"Saved attachment: {filepath}")
            except Exception:
                logging.exception(f"Failed to save attachment: {filename}")
    return file_paths
