from src.webapp.db import db
from datetime import datetime, timezone
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()
FERNET_KEY = os.environ.get("FERNET_KEY")
fernet = Fernet(FERNET_KEY)



class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    internship = db.Column(db.String(100), nullable=True)
    applied_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    read = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)  # Store full email body

    attachments = db.relationship("Attachment", back_populates="candidate", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Candidate {self.name} ({self.email})>"


class Attachment(db.Model):
    __tablename__ = "attachments"

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=True)
    path = db.Column(db.String(500), nullable=False)
    uploaded_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    candidate = db.relationship("Candidate", back_populates="attachments")

    def __repr__(self):
        return f"<Attachment {self.filename} for {self.candidate.name}>"


class Setting(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)

    # Email/IMAP settings
    imap_server = db.Column(db.String(255), nullable=False, default="imap.gmail.com")
    email_user = db.Column(db.String(255), nullable=False)
    _email_pass = db.Column(db.LargeBinary, nullable=False)
    folder = db.Column(db.String(50), default="INBOX")
    search_criteria = db.Column(db.String(50), default="UNSEEN")
    timeout_seconds = db.Column(db.Integer, default=30)

    # Storage / attachment folder
    attachment_folder = db.Column(db.String(255), default="attachments")

    # Internship code mapping (JSON string)
    internship_code_map = db.Column(db.Text, default='{"PY": "Python Developer", "WD": "Web Developer", "GD": "Graphic Designer", "ML": "Machine Learning Intern"}')

    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    # Email password encryption handling
    @property
    def email_pass(self):
        return fernet.decrypt(self._email_pass).decode()

    @email_pass.setter
    def email_pass(self, plaintext: str):
        self._email_pass = fernet.encrypt(plaintext.encode())

    def __repr__(self):
        return f"<Setting {self.email_user} @ {self.imap_server}>"

