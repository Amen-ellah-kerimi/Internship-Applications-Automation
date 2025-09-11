from src.webapp.app import db
from src.webapp.models import Candidate , Setting
import src.webapp.scraper as scraper

# ------------------------
# Candidates
# ------------------------
def fetch_candidates():
    """Return all candidates ordered by applied date desc"""
    return Candidate.query.order_by(Candidate.applied_on.desc()).all()

def get_candidate_details(candidate_id):
    """Return candidate and their attachments"""
    candidate = Candidate.query.get_or_404(candidate_id)
    attachments = candidate.attachments
    return candidate, attachments

def scrape_and_save_candidates():
    """
    Run the scraper using settings from DB
    and save candidates + attachments
    Returns number of new candidates added
    """
    setting = get_settings()
    if not getattr(setting, 'email_user', None) or not getattr(setting, 'email_pass', None):
        return {"error": "Email and password are not configured."}
    result = scraper.fetch_and_save_emails(
        imap_server=setting.imap_server,
        email_user=setting.email_user,
        email_pass=setting.email_pass,
        folder=setting.folder
    )
    return result

# ------------------------
# Settings
# ------------------------
def get_settings():
    """Return the single settings object or create default"""
    setting = Setting.query.first()
    if not setting:
        # Create default settings
        setting = Setting(
            imap_server="imap.gmail.com",
            email_user="",
            email_pass="changeme",
            folder="INBOX",
            attachment_folder="attachments"
        )
        db.session.add(setting)
        db.session.commit()
    return setting

def update_settings(imap_server, email_user, email_pass, folder, attachment_folder=None, internship_code_map=None):
    """Update settings in the DB"""
    setting = get_settings()
    setting.imap_server = imap_server
    setting.email_user = email_user
    setting.email_pass = email_pass
    setting.folder = folder
    if attachment_folder is not None:
        setting.attachment_folder = attachment_folder
    if internship_code_map is not None:
        setting.internship_code_map = internship_code_map
    db.session.commit()

