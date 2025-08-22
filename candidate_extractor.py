import re

def extract_candidate_info(body):
    if not body:
        return None

    candidate = {}
    # Example regex patterns
    name_match = re.search(r"Name[:\s]+(.+)", body, re.IGNORECASE)
    email_match = re.search(r"Email[:\s]+([\w\.-]+@[\w\.-]+)", body, re.IGNORECASE)
    phone_match = re.search(r"Phone[:\s]+(\+?\d+)", body, re.IGNORECASE)
    linkedin_match = re.search(r"(https?://www.linkedin.com/in/[^\s]+)", body, re.IGNORECASE)

    if name_match: candidate["name"] = name_match.group(1).strip()
    if email_match: candidate["email"] = email_match.group(1).strip()
    if phone_match: candidate["phone"] = phone_match.group(1).strip()
    if linkedin_match: candidate["linkedin"] = linkedin_match.group(1).strip()

    return candidate if candidate else None

