
"""
Internship Scraper Library

Exposes high-level API functions for CLI, Flask, and scripts.

Notes:
	- Use run_scraper and save_to_csv for main workflows.
	- All config is loaded from YAML and can be overridden.
	- See individual modules for details and extension points.
"""

from .main import run_scraper, save_to_csv