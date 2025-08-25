# Contributing Guide: Internship Applications Automation

Welcome! This guide will help you get started, contribute, and maintain the Internship Applications Automation project. It is designed for interns, developers, and supervisors in a company setting.

---

## 🚀 Project Overview
This tool automates the extraction of internship candidate data from emails and stores it in a structured CSV file. It supports attachments, robust error handling, and logging for traceability.

---

## 🛠️ Getting Started
1. **Clone the repository**
2. **Set up your environment:**
   - Copy `.env.example` to `.env` and fill in your email credentials.
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
3. **Run the script:**
   - Start with:
     ```bash
     python main.py
     ```
   - The script will check for new internship applications every 5 minutes by default.
   - For production, use cron or systemd for scheduled runs.

---

## 🧩 Code Structure
- `main.py`: Orchestrates the workflow, logging, and background checking.
- `email_client.py`: Handles email connection and mailbox operations.
- `parser.py`: Parses emails and extracts attachments.
- `candidate_extractor.py`: Extracts candidate info from email body.
- `csv_handler.py`: Manages CSV creation and appending.
- `utils.py`: Helper functions (e.g., timestamp).

---

## 📝 Coding Standards
- **Logging:** Use Python's `logging` for all actions, warnings, and errors.
- **Error Handling:** Wrap critical operations in `try/except` and log exceptions.
- **Comments:** Use `TODO`, `NOTE`, and `FIXME` for future work, clarifications, and known issues.
- **Modularity:** Keep code organized by feature/module.

---

## 🧪 Testing & Validation
- Test with sample emails (including attachments and malformed subjects).
- Check `candidates.csv` for correct and complete data.
- Review logs for errors and warnings.

---

## 🔄 Extending the Project
- To add new CSV fields, update `CSV_FIELDS` in `csv_handler.py` and extraction logic in `candidate_extractor.py`.
- To support new internship codes, update `code_map` in `parser.py`.
- For new features, add TODOs and document your changes.

---

## 👥 Collaboration
- Commit with clear messages.
- Open issues for bugs, enhancements, or questions.
- Review and test before merging changes.

---

## 📚 Resources
- [README.md](./README.md): Project features, workflow, and setup.
- [Python Logging Docs](https://docs.python.org/3/library/logging.html)
- [IMAP Protocol](https://datatracker.ietf.org/doc/html/rfc3501)

---

## 💬 Support
For help, open an issue or contact the project maintainer.
