# Project Overview: Internship Applications Automation

---

## Purpose
Automates the extraction of internship candidate data from emails and stores it in a structured CSV file. It reduces manual work, ensures data consistency, and centralizes applicant information.

---

## Main Features
- **Automatic Email Scraping:** Connects to Gmail/Outlook via IMAP, fetches unread internship application emails.
- **Targeted Filtering:** Processes emails with subject format: `Internship Application - Name - CODE`.
- **Candidate Data Extraction:** Extracts name, email, phone, LinkedIn, subject, sender, received date, notes, and CV/attachments.
- **CSV Storage:** Saves candidate data in `candidates.csv`, avoiding duplicates.
- **Logging & Error Handling:** Uses Python’s logging for all major actions and errors.
- **Modular Architecture:** Split into reusable modules for email, parsing, extraction, CSV handling, and utilities.

---

## Workflow
1. Connect to email inbox using credentials from `.env`.
2. Fetch unread emails matching the internship application subject pattern.
3. Parse email content, extract candidate info and attachments.
4. Append data to `candidates.csv`.
5. Mark emails as read.
6. Log all actions and errors.

---

## Code Structure
- `main.py`: Orchestrates the workflow, logging, and background checking.
- `email_client.py`: Handles email connection and mailbox operations.
- `parser.py`: Parses emails and extracts attachments.
- `candidate_extractor.py`: Extracts candidate info from email body.
- `csv_handler.py`: Manages CSV creation and appending.
- `utils.py`: Helper functions (e.g., timestamp).

---

## Tech Stack
- **Python 3.10+**
- **IMAP** (for email handling)
- **python-dotenv** (for environment management)

---

## How to Run
1. Copy `.env.example` to `.env` and fill in your email credentials.
2. Install dependencies:  
   `pip install -r requirements.txt`
3. Run the script:  
   `python main.py`
4. The script checks for new emails every 5 minutes (can be scheduled with cron/systemd).

---

## Extending & Contributing
- Add new CSV fields by updating `CSV_FIELDS` in `csv_handler.py` and extraction logic in `candidate_extractor.py`.
- Support new internship codes by updating `code_map` in `parser.py`.
- See `CONTRIBUTING.md` for coding standards and contribution guidelines.

---

## Example Output
A sample row in `candidates.csv`:
```
name,email,phone,linkedin,subject,sender,received_date,notes,cv
Jane Doe,jane.doe@example.com,+1234567890,https://www.linkedin.com/in/janedoe,Internship Application - Jane Doe - PY,Amen Ellah Kerimi mamap4110@gmail.com,2025-08-22 12:57:22,,attachments/jane_doe_cv.pdf
```

---

## Future Enhancements
- Map internship codes to human-readable types.
- Advanced reporting.
- More robust duplicate detection.
- Support for more attachment types.

---

## Support
For questions or suggestions, open an issue or contact the maintainer.
