"""
General IMAP Email Scraper Library

Provides modular functions and classes for connecting to IMAP, searching, fetching, parsing, and saving emails and attachments.
Can be used as a CLI tool or imported as a library.
"""

from .imap import IMAPClient, EmailMessage, Attachment