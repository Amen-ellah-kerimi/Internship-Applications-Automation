"""
Console logger with colored output using Python's built-in logging module.

Provides convenient module-level methods for logging messages at different levels:
- console.log
- console.warn
- console.error
- console.debug

Notes:
    - Uses Python logging internally for thread safety and Flask compatibility.
"""

import logging
import sys
from typing import Optional
from colorama import init, Fore, Style
import json


logger = logging.getLogger("console_logger")
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
# initialize colorama at startup
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)

        match record.levelno:
            case logging.DEBUG:
                return f"{Fore.BLUE}{msg}{Style.RESET_ALL}"
            case logging.INFO:
                return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"
            case logging.WARNING:
                return f"{Fore.YELLOW}{msg}{Style.RESET_ALL}"
            case logging.ERROR:
                return f"{Fore.RED}{msg}{Style.RESET_ALL}"
            case logging.CRITICAL:
                return f"{Fore.MAGENTA}{msg}{Style.RESET_ALL}"
            case _:
                return msg

console_handler.setFormatter(ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"))
if not logger.hasHandlers():
    logger.addHandler(console_handler)

def _format_message(message: str, metadata: Optional[dict]) -> str:
    if metadata:
        # safely serialize metadata as JSON
        metadata_str = json.dumps(metadata, default=str) # default=str to handle non-serializable objects
        return f"{message} | Metadata: {metadata_str}"
    return message


class Console:
    """
    Module-level console object that maps directly to logging functions.

    """

    def log(self, message: str, metadata: Optional[dict] = None) -> None:
        """
        Log an INFO-level message.

        Args:
            message (str): The message to log.
            metadata (dict, optional): Additional metadata to include in logs.

        Notes:
            - Displayed in green in the console.
        """
        logger.info(_format_message(message, metadata))

    def warn(self, message: str, metadata: Optional[dict] = None) -> None:
        """
        Log a WARNING-level message.

        Args:
            message (str): The message to log.
            metadata (dict, optional): Additional metadata to include in logs.

        Notes:
            - Displayed in yellow in the console.
        """
        logger.warning(_format_message(message, metadata))

    def warning(self, message: str, metadata: Optional[dict] = None) -> None:
        """
        Alias for warn() to match logging module's naming.

        Args:
            message (str): The message to log.
            metadata (dict, optional): Additional metadata to include in logs.
        """
        self.warn(message, metadata)


    def error(self, message: str, metadata: Optional[dict] = None) -> None:
        """
        Log an ERROR-level message.

        Args:
            message (str): The message to log.
            metadata (dict, optional): Additional metadata to include in logs.

        Notes:
            - Displayed in red in the console.
        """
        logger.error(_format_message(message, metadata))


    def debug(self, message: str, metadata: Optional[dict] = None) -> None:
        """
        Log a DEBUG-level message.

        Args:
            message (str): The message to log.
            metadata (dict, optional): Additional metadata to include in logs.

        Notes:
            - Displayed in blue in the console.
        """
        logger.debug(_format_message(message, metadata))

    def critical(self, message: str, metadata: Optional[dict] = None) -> None:
        """
        Log a CRITICAL-level message.

        Args:
            message (str): The message to log.
            metadata (dict, optional): Additional metadata to include in logs.

        Notes:
            - Displayed in magenta in the console.
        """
        logger.critical(_format_message(message, metadata))



# Ready-to-use logger object
console = Console()


# Use like:
#   from utils.logger import console
#   console.log("Info message")
#   console.warn("Warning!")
#   console.error("Error!")
#   console.debug("Debug info")
