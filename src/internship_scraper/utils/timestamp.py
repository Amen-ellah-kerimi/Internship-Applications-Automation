
from datetime import datetime
import logging

def timestamp_now(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get the current timestamp as a formatted string.

    Args:
        fmt (str): Format string for datetime. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: Current timestamp formatted as a string.

    Notes:
        - NOTE: Used for logging and CSV fields.
        - TODO: Make format configurable via config if needed.
        - FIXME: No timezone support; always local time.
    """
    try:
        return datetime.now().strftime(fmt)
    except Exception:
        logging.exception("Error formatting timestamp")
        return "N/A"

