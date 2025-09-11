# Getting Started: Dashboard Setup

## Files to Create
- `app.py` — Flask web app entry point
- `templates/dashboard.html` — HTML template for the dashboard
- (Optional) `static/` — for CSS or JS if needed

## Setup Steps
1. **Install Flask:**
   ```bash
   pip install flask
   ```
2. **Create Flask App:**
   - Add basic Flask app code in `app.py`
   - Set up routes:
     - `/` — Dashboard homepage (shows table, buttons)
     - `/run-scraper` — Triggers scraping process
     - `/export-csv` — Downloads/export CSV file
3. **Reuse Scraping Logic:**
   - Import and call your existing scraping functions from the dashboard
4. **Create HTML Template:**
   - Simple table for results
   - Buttons for actions
5. **Run the App:**
   ```bash
   python app.py
   ```
6. **Access Dashboard:**
   - Open browser at `http://localhost:5000`

## Next Steps
- Add TODO, FIXME, NOTE comments in new and existing code
- Follow the checklist in `task.md`
