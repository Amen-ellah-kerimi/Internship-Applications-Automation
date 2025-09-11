
import argparse
import logging
from pathlib import Path
from .main import run_scraper, save_to_csv

def main() -> None:
    """
    CLI entry point for internship scraper.

    Parses command-line arguments, runs the scraper, and saves results to CSV.

    Notes:
        - TODO: Add argument validation and error handling.
        - FIXME: Logging configuration is basic; add file logging if needed.
        - NOTE: CLI args override config settings.
    """
    parser = argparse.ArgumentParser(description="Run internship scraper")
    parser.add_argument("-e", "--email", type=str, help="Email to connect")
    parser.add_argument("-p", "--password", type=str, help="Email password or app token")
    parser.add_argument("-f", "--folder", type=str, help="Mailbox folder to check (default from config)")
    parser.add_argument("-c", "--code", type=str, help="Internship code to filter")
    parser.add_argument("-o", "--output", type=str, help="Path to save CSV file (default: ./candidates.csv)")
    parser.add_argument("--config", type=str, default="defaults/email_config.yaml", help="Path to config YAML")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    # Determine output path
    output_path = args.output if args.output else "candidates.csv"

    # Build overrides from CLI args
    overrides = {}
    if args.email:
        overrides["email_user"] = args.email
    if args.password:
        overrides["email_pass"] = args.password
    if args.folder:
        overrides["email_folder"] = args.folder
    if args.code:
        overrides["internship_code"] = args.code

    # Run scraper
    candidates = run_scraper(config_path=args.config, overrides=overrides)

    # Save to CSV
    save_to_csv(candidates, path=output_path)

    logging.info(f"Scraping complete. Saved {len(candidates)} candidates to {Path(output_path).resolve()}")
