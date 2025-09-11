# Internship Applications Automation - Project Overview

## Purpose
Automate the process of scraping internship applications from email, storing candidate data and attachments in a database, and providing a modern web dashboard for management.

## Main Features
- Modular Flask web application (`src/webapp`) with SQLAlchemy ORM
- Candidate, Attachment, and Setting models with secure password handling
- Email scraper to fetch, parse, and save candidate data and attachments
- Responsive dashboard UI with sortable tables, candidate detail, and settings pages
- Service layer for business logic and database operations
- Project documentation and configuration via `docs/` and `pyproject.toml`


## Project Checklist

- [x] Modular Flask webapp structure in `src/webapp`
- [x] SQLAlchemy ORM integration and single `db` instance
- [x] Candidate, Attachment, and Setting models
- [x] Email scraper for candidate and attachment extraction
- [x] Service layer for business logic
- [x] Responsive dashboard UI with sortable tables
- [x] Candidate detail and settings pages
- [x] Project documentation in `docs/`
- [x] Python project configuration in `pyproject.toml`
- [x] Database stored in `instance/database.db`
- [x] Development tools: `black`, `isort`, `flake8`, `pytest`
- [x] CONTRIBUTING guidelines
- [ ] Add unit tests for scraper and services
- [ ] Add deployment instructions for production
- [ ] Add API endpoints for integration (optional)

## Project Structure
```
career/
├── docs/                # Documentation, onboarding, technical notes
├── pyproject.toml       # Python project configuration
├── requirements.txt     # Additional dependencies
├── src/
│   ├── internship_scraper/   # Legacy scripts and CLI tools
│   └── webapp/               # Flask web application
│       ├── app.py            # Main Flask app
│       ├── db.py             # SQLAlchemy instance
│       ├── models.py         # ORM models
│       ├── routes.py         # Route registration
│       ├── scraper.py        # Email scraping logic
│       ├── services.py       # Business logic
│       ├── static/           # CSS/JS assets
│       └── templates/        # Jinja2 HTML templates
│       └── instance/         # Database file
```

## Setup & Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Flask app from the project root:
   ```bash
   python -m src.webapp.app
   ```
3. Access the dashboard at [http://localhost:5000](http://localhost:5000)

## Configuration
- Project metadata and dependencies are managed in `pyproject.toml`.
- Environment variables (e.g., `FLASK_SECRET_KEY`, `FERNET_KEY`) can be set for security.
- Database is stored in `src/webapp/instance/database.db`.

## Development Tools
- Formatting: `black`, `isort`
- Linting: `flake8`
- Testing: `pytest`

## Contributing
See `CONTRIBUTING.md` for guidelines.

## Authors
- Amen Ellah Kerimi <mamap4110@gmail.com>
