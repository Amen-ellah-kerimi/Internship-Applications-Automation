# [![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=F7F7F7&width=600&lines=Internship+Applications+Automation)](https://git.io/typing-svg)

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![IMAP](https://img.shields.io/badge/IMAP-%23007396?style=for-the-badge)](https://tools.ietf.org/html/rfc3501)
[![dotenv](https://img.shields.io/badge/dotenv-%233476A1?style=for-the-badge)](https://github.com/theskumar/python-dotenv)
[![CSV](https://img.shields.io/badge/CSV-FF6C37?style=for-the-badge)](https://en.wikipedia.org/wiki/Comma-separated_values)


This project automates the collection of internship candidates’ data from emails and stores it in a structured CSV file. It reduces manual work, ensures data consistency, and provides a central repository for all applicants.

---

## 📝 Features

- **Automatic Email Scraping:** Connects to Gmail/Outlook inbox via IMAP and fetches unread internship application emails.
- **Targeted Filtering:** Processes only emails with the subject format: `Internship Application - Name - CODE`.
- **Candidate Data Extraction:** Extracts:
  - Name
  - Email
  - Phone number
  - LinkedIn/Portfolio links
  - Email subject and sender
  - Received date
  - Notes
- **CSV Storage:** Saves structured candidate data in `candidates.csv` while avoiding duplicates.
- **Modular Architecture:** Code split into reusable modules:
  - `email_client.py` — email connection and fetching
  - `parser.py` — email parsing
  - `candidate_extractor.py` — candidate info extraction
  - `csv_handler.py` — CSV management
  - `utils.py` — helper functions

---

## 📈 Workflow

1. Connect to email inbox using credentials in `.env`.
2. Fetch unread emails with the internship application subject pattern.
3. Parse email content and extract candidate info.
4. Append data to `candidates.csv`.
5. Mark emails as read.

---

## 📂 Example Output

<img width="1895" height="309" alt="Example Output" src="https://github.com/user-attachments/assets/dfef919e-d282-4eec-a4ca-cc02e96379ef" />

CSV sample:
name,email,phone,linkedin,subject,sender,received_date,notes
Jane Doe,jane.doe@example.com
,+1234567890,https://www.linkedin.com/in/janedoe,Internship
 Application - Jane Doe - 101,Amen Ellah Kerimi mamap4110@gmail.com
,2025-08-22 12:57:22,


---

## 💻 Tech Stack

### Programming
[![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)

### Email Handling
[![IMAP](https://img.shields.io/badge/IMAP-007ACC?style=for-the-badge&logo=email&logoColor=white)](https://datatracker.ietf.org/doc/html/rfc3501)

### Environment Management
[![dotenv](https://img.shields.io/badge/python--dotenv-000000?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/python-dotenv/)

---

## ⚡ Future Enhancements

- Map internship codes to human-readable **internship types**.
- Validate candidate entries to prevent duplicates.
- Support **attachments** (CVs, portfolios, etc.).
- Add logging and reporting features.

---

## ⚙️ Requirements

- Python 3.10+
- `imaplib` (standard library)
- `python-dotenv`

Install dependencies:

```bash
pip install -r requirements.txt
