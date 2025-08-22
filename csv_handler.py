import csv
import os

CSV_FIELDS = ["name", "email", "phone", "linkedin", "subject", "sender", "received_date", "notes"]

def init_csv(csv_path):
    if not os.path.exists(csv_path):
        with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()

def append_candidate(csv_path, candidate):
    init_csv(csv_path)
    with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(candidate)

