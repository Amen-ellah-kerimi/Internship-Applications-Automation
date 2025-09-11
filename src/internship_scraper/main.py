
import logging
from typing import List, Dict, Any, Optional, Callable
from .email_client import validate_email_creds, connect_email, fetch_unread_emails, mark_email_read
from .parser import parse_email, save_attachments
from .candidate_extractor import extract_candidate_info
from .csv_handler import save_to_csv
from .utils.timestamp import timestamp_now
from .config_loader import get_config

def run_scraper(
    config_path: str = "defaults/email_config.yaml",
    overrides: Optional[Dict[str, Any]] = None,
    on_candidate: Optional[Callable[[Dict[str, Any]], None]] = None
) -> List[Dict[str, Any]]:
    """
    High-level API to run the internship scraper.

    Connects to the email server, fetches unread emails, parses them, extracts candidate info, and returns a list of candidates.

    Args:
        config_path (str): Path to the config YAML file.
        overrides (Optional[Dict[str, Any]]): Dict of config overrides (email, password, folder, etc.).
        on_candidate (Optional[Callable[[Dict[str, Any]], None]]): Callback for each processed candidate.

    Returns:
        List[Dict[str, Any]]: List of candidate dictionaries.

    Notes:
        - NOTE: Stateless, thread-safe, and Flask-friendly. No blocking loops or global state.
        - TODO: Add batch options and error handling improvements.
        - FIXME: No retry logic for failed email fetches.
    """
    config = get_config(config_path)
    if overrides:
        config.update(overrides)
    user = config.get("email_user")
    password = config.get("email_pass")
    server = config.get("imap_server")
    folder = config.get("email_folder", "inbox")

    validate_email_creds(user, password)
    mail = connect_email(user, password, server)
    messages = fetch_unread_emails(mail, folder=folder)
    candidates = []
    for msg_id in messages:
        try:
            _, msg_data = mail.fetch(msg_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg_dict = parse_email(response_part[1])
                    attachment_paths = save_attachments(msg_dict["attachments"], config_path=config_path)
                    candidate = extract_candidate_info(msg_dict["body"], msg_dict["sender"])
                    if candidate:
                        candidate.update({
                            "subject": msg_dict["subject"],
                            "sender": msg_dict["sender"],
                            "received_date": timestamp_now(),
                            "notes": "",
                            "cv": attachment_paths[0] if attachment_paths else "N/A"
                        })
                        candidates.append(candidate)
                        if on_candidate:
                            on_candidate(candidate)
                    mark_email_read(mail, msg_id)
        except Exception:
            logging.exception("Error processing email message")
    logging.info(f"Processed {len(candidates)} candidates.")
    return candidates

def save_to_csv(candidates: List[Dict[str, Any]], path: str = "candidates.csv") -> None:
    """
    Save a list of candidate dictionaries to a CSV file.

    Args:
        candidates (List[Dict[str, Any]]): List of candidate dictionaries.
        path (str): Path to the CSV file.

    Returns:
        None

    Notes:
        - NOTE: Stateless and Flask-friendly. Does not block or use global state.
        - TODO: Add error handling for file write failures.
    """
    save_to_csv(candidates, path=path)

