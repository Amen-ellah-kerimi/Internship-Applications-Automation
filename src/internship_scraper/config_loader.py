from typing import Any
from src.internship_scraper.utils.logger import console

class ConfigLoader:
    """
    Loads app settings from the database and provides a dict-like interface.
    """

    def __init__(self):
        self._settings = None

    def load(self) -> dict[str, Any]:
        """Load settings from DB. Returns a plain dict."""
        settings_row = Settings.query.first()
        if not settings_row:
            console.warn("No settings found in DB, using empty defaults.")
            self._settings = {}
            return self._settings

        # Convert SQLAlchemy object to dict
        self._settings = {
            "imap_server": settings_row.imap_server,
            "email_user": settings_row.email_user,
            "email_pass": settings_row.email_pass,  # decrypted property
            "folder": settings_row.folder,
            "search_criteria": settings_row.search_criteria,
            "timeout_seconds": settings_row.timeout_seconds,
            "csv_path": settings_row.csv_path,
            "fields": settings_row.fields,
            "duplicate_check_field": settings_row.duplicate_check_field,
            "delimiter": settings_row.delimiter,
            "encoding": settings_row.encoding,
            "subject_pattern": settings_row.subject_pattern,
            "code_map": settings_row.code_map,
            "default_values": settings_row.default_values,
            "attachment_folder": settings_row.attachment_folder,
        }

        console.log("Settings loaded from DB.")
        return self._settings

    def get(self, key: str, default=None):
        """Get nested config using dot notation, e.g., 'email_user'."""
        if not self._settings:
            self.load()
        return self._settings.get(key, default)

    @property
    def settings(self) -> dict[str, Any]:
        """Get all settings as a dict."""
        if not self._settings:
            self.load()
        return self._settings
# singleton loader
config_loader = ConfigLoader()

