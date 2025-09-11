import re
import logging
from typing import Dict, Any, Optional, List, Callable
from .config_loader import get_config

def extract_candidate_info(
    body: str,
    sender_email: str,
    internship_code_map: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Extract candidate information from email body and sender email.

    Args:
        body (str): The raw email body to parse.
        sender_email (str): The sender's email address.
        internship_code_map (Optional[Dict[str, str]]): Mapping of internship codes to names. If None, loads from config.

    Returns:
        Dict[str, Any]: Dictionary containing extracted candidate information.

    Notes:
        - NOTE: Assumes email body is plain text. For HTML, parsing should be added.
        - TODO: Add argument validation and error handling for malformed emails.
        - FIXME: Regex patterns may miss edge cases or non-standard formats.
    """
    if internship_code_map is None:
        config = get_config("defaults/rules.yaml")
        internship_code_map = config.get("internship_code_map", {})

    if not body:
        logging.warning("Email body missing, using defaults.")
        # TODO: Consider raising an exception or returning None for missing body
        return {
            "name": "N/A",
            "email": sender_email,
            "phone": "N/A",
            "linkedin": "N/A",
            "internship": "N/A"
        }
    candidate = {}
    try:
        name_match = re.search(r"Name[:\s]+(.+)", body, re.IGNORECASE)
        phone_match = re.search(r"Phone[:\s]+(\+?\d+)", body, re.IGNORECASE)
        linkedin_match = re.search(r"(https?://www.linkedin.com/in/[^\s]+)", body, re.IGNORECASE)
        code_match = re.search(r"Internship Code[:\s]+(\w+)", body, re.IGNORECASE)
        candidate["name"] = name_match.group(1).strip() if name_match else "N/A"
        candidate["email"] = sender_email
        candidate["phone"] = phone_match.group(1).strip() if phone_match else "N/A"
        candidate["linkedin"] = linkedin_match.group(1).strip() if linkedin_match else "N/A"
        code = code_match.group(1).strip() if code_match else None
        candidate["internship"] = internship_code_map.get(code, code) if code else "N/A"
        # TODO: Add more fields as needed (university, graduation year, etc.)
        # FIXME: This assumes fields are always present and formatted correctly
        logging.debug(f"Extracted candidate: {candidate}")
        return candidate
    except Exception:
        logging.exception("Error extracting candidate info")
        return {
            "name": "N/A",
            "email": sender_email,
            "phone": "N/A",
            "linkedin": "N/A",
            "internship": "N/A"
        }

def extract_candidates_from_emails(
    email_bodies: List[str],
    sender_emails: List[str],
    internship_code_map: Optional[Dict[str, str]] = None,
    on_candidate: Optional[Callable[[Dict[str, Any]], None]] = None
) -> List[Dict[str, Any]]:
    """
    Extract candidate information from lists of email bodies and sender emails.

    Args:
        email_bodies (List[str]): List of raw email bodies.
        sender_emails (List[str]): List of sender email addresses.
        internship_code_map (Optional[Dict[str, str]]): Mapping of internship codes to names. If None, loads from config.
        on_candidate (Optional[Callable[[Dict[str, Any]], None]]): Callback invoked for each processed candidate.

    Returns:
        List[Dict[str, Any]]: List of candidate dictionaries.

    Notes:
        - NOTE: Designed for batch processing; stateless and thread-safe.
        - TODO: Add parallel processing for large batches.
        - FIXME: Assumes email_bodies and sender_emails are aligned by index.
    """
    candidates = []
    for body, sender in zip(email_bodies, sender_emails):
        candidate = extract_candidate_info(body, sender, internship_code_map)
        candidates.append(candidate)
        if on_candidate:
            on_candidate(candidate)
    logging.info(f"Extracted {len(candidates)} candidates from emails.")
    return candidates
