import csv
import os
import logging
CSV_FIELDS = ["name", "email", "phone", "linkedin", "subject", "sender", "received_date", "notes", "cv"]

def init_csv(csv_path):
    try:
        if not os.path.exists(csv_path):
            with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
                writer.writeheader()
    except Exception:
        logging.exception(f"Error initializing CSV file: {csv_path}")

def append_candidate(csv_path, candidate):
    init_csv(csv_path)
    try:
        with open(csv_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'] == candidate['email']:
                    logging.info(f"Candidate with email {candidate['email']} already exists in {csv_path}")
                    return
        with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writerow(candidate)
        logging.info(f"Candidate {candidate['name']} added to {csv_path}")
    except Exception:
        logging.exception(f"Error appending candidate to CSV: {csv_path}")

