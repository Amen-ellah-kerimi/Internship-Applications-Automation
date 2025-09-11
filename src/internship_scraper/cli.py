import argparse
import os
import csv
import logging
from . import IMAPClient

def save_attachments(attachments, folder):
    """Save attachments to disk and return list of saved file paths."""
    os.makedirs(folder, exist_ok=True)
    saved_files = []
    for att in attachments:
        if att.filename and att.data:
            file_path = os.path.join(folder, att.filename)
            try:
                with open(file_path, 'wb') as f:
                    f.write(att.data)
                saved_files.append(file_path)
            except Exception as e:
                logging.error(f"Failed to save attachment {att.filename}: {e}")
    return saved_files

def main():
    """Run the IMAP email scraper CLI."""
    parser = argparse.ArgumentParser(description="General IMAP Email Scraper CLI")
    parser.add_argument('--imap-server', type=str, required=True, help='IMAP server (e.g. imap.gmail.com)')
    parser.add_argument('--email-user', type=str, required=True, help='Email user')
    parser.add_argument('--email-pass', type=str, required=True, help='Email password or app token')
    parser.add_argument('--folder', type=str, default='INBOX', help='IMAP folder')
    parser.add_argument('--attachment-folder', type=str, default='attachements', help='Folder to save attachments')
    parser.add_argument('--csv-path', type=str, default='emails.csv', help='CSV file to save emails')
    parser.add_argument('--search', type=str, default='UNSEEN', help='IMAP search criteria')
    parser.add_argument('--log-level', type=str, default='INFO', help='Logging level (DEBUG, INFO, WARNING, ERROR)')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO),
                        format='%(asctime)s %(levelname)s %(message)s')

    try:
        client = IMAPClient(args.imap_server, args.email_user, args.email_pass, args.folder)
        client.connect()
        msg_ids = client.search(args.search)
        emails = []
        for msg_id in msg_ids:
            email_msg = client.fetch_email(msg_id)
            if email_msg:
                saved_files = save_attachments(email_msg.attachments, args.attachment_folder)
                emails.append({
                    "subject": email_msg.subject,
                    "sender": email_msg.sender,
                    "body": email_msg.body,
                    "attachments": ", ".join(saved_files)
                })
                client.mark_read(msg_id)
        client.logout()
        # Save to CSV
        fieldnames = ["subject", "sender", "body", "attachments"]
        with open(args.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for email_row in emails:
                writer.writerow(email_row)
        logging.info(f"Saved {len(emails)} emails to {args.csv_path}")
    except Exception as e:
        logging.error(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
