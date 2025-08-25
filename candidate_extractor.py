import re
import logging

def extract_candidate_info(body, sender_email):
    if not body:
        logging.warning("Email body missing, using defaults.")
        return {
            "name": "N/A",
            "email": sender_email,
            "phone": "N/A",
            "linkedin": "N/A"
        }
    candidate = {}
    try:
        name_match = re.search(r"Name[:\s]+(.+)", body, re.IGNORECASE)
        phone_match = re.search(r"Phone[:\s]+(\+?\d+)", body, re.IGNORECASE)
        linkedin_match = re.search(r"(https?://www.linkedin.com/in/[^\s]+)", body, re.IGNORECASE)
        candidate["name"] = name_match.group(1).strip() if name_match else "N/A"
        candidate["email"] = sender_email
        candidate["phone"] = phone_match.group(1).strip() if phone_match else "N/A"
        candidate["linkedin"] = linkedin_match.group(1).strip() if linkedin_match else "N/A"
        return candidate
    except Exception:
        logging.exception("Error extracting candidate info")
        return {
            "name": "N/A",
            "email": sender_email,
            "phone": "N/A",
            "linkedin": "N/A"
        }
