
import csv
import os
import logging
from typing import List, Dict, Any, Optional
from .config_loader import get_config

def get_csv_fields(config_path: str = "defaults/csv_config.yaml") -> List[str]:
    """
    Get the list of CSV fields from config.

    Args:
        config_path (str): Path to the CSV config YAML file.

    Returns:
        List[str]: List of field names for the CSV.

    Notes:
        - NOTE: Defaults to standard fields if config is missing.
        - TODO: Validate config structure and handle missing fields.
    """
    try:
        config = get_config(config_path)
        return config.get("fields", ["name", "email", "phone", "linkedin", "subject", "sender", "received_date", "notes", "cv"])
    except Exception:
        logging.exception(f"Error loading CSV fields from config: {config_path}")
        return ["name", "email", "phone", "linkedin", "subject", "sender", "received_date", "notes", "cv"]

def init_csv(csv_path: str, fields: Optional[List[str]] = None) -> None:
    """
    Initialize a CSV file with headers if it does not exist.

    Args:
        csv_path (str): Path to the CSV file.
        fields (Optional[List[str]]): List of field names. If None, loads from config.

    Returns:
        None

    Notes:
        - TODO: Add argument validation for csv_path and fields.
        - FIXME: Does not handle concurrent writes.
    """
    if fields is None:
        fields = get_csv_fields()
    try:
        if not os.path.exists(csv_path):
            with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
    except Exception:
        logging.exception(f"Error initializing CSV file: {csv_path}")

def save_to_csv(candidates: List[Dict[str, Any]], path: str = "candidates.csv", fields: Optional[List[str]] = None) -> None:
    """
    Save a list of candidate dictionaries to a CSV file.

    Args:
        candidates (List[Dict[str, Any]]): List of candidate dictionaries.
        path (str): Path to the CSV file.
        fields (Optional[List[str]]): List of field names. If None, loads from config.

    Returns:
        None

    Notes:
        - NOTE: Overwrites the file with all candidates.
        - TODO: Add append mode and duplicate checking if needed.
        - FIXME: No atomic write; may cause data loss if interrupted.
    """
    if fields is None:
        fields = get_csv_fields()
    try:
        with open(path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for candidate in candidates:
                writer.writerow(candidate)
        logging.info(f"Saved {len(candidates)} candidates to {path}")
    except Exception:
        logging.exception(f"Error saving candidates to CSV: {path}")

def append_candidate(csv_path: str, candidate: Dict[str, Any], fields: Optional[List[str]] = None) -> None:
    """
    Append a candidate dictionary to a CSV file, avoiding duplicates by email.

    Args:
        csv_path (str): Path to the CSV file.
        candidate (Dict[str, Any]): Candidate dictionary to append.
        fields (Optional[List[str]]): List of field names. If None, loads from config.

    Returns:
        None

    Notes:
        - NOTE: Checks for duplicate email before appending.
        - TODO: Optimize for large files (avoid full scan).
        - FIXME: Not thread-safe for concurrent writes.
    """
    if fields is None:
        fields = get_csv_fields()
    init_csv(csv_path, fields)
    try:
        with open(csv_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('email') == candidate.get('email'):
                    logging.info(f"Candidate with email {candidate.get('email')} already exists in {csv_path}")
                    return
        with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writerow(candidate)
        logging.info(f"Candidate {candidate.get('name', 'N/A')} added to {csv_path}")
    except Exception:
        logging.exception(f"Error appending candidate to CSV: {csv_path}")

