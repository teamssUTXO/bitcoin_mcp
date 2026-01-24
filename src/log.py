import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional

from src.config import Config


# Docs : https://docs.python.org/3/library/logging.html
class LoggerMCP:
    """Server Logger Class"""
    def __init__(self):
        self.logger_name: str = Config.LOGGER_NAME
        self.log_dir: Path = Path(Config.LOG_DIR)
        self.level: str = Config.LOG_LEVEL
        self.backup_count: int = Config.LOGGER_BACKUP_COUNT
        self.console_output: bool = Config.LOGGER_CONSOLE_OUTPUT

        self.root_logger: logging.Logger = logging.getLogger()

        self._setup_logger()

    def _setup_logger(self) -> None:
        """Setup the Logger"""
        self.log_dir.mkdir(parents=True, exist_ok=True)

        log_level = getattr(logging, self.level.upper(), logging.INFO)

        self.root_logger.setLevel(log_level)
        self.root_logger.handlers.clear()

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = TimedRotatingFileHandler(
            filename=self.log_dir / "server.log",
            utc=True,
            when="midnight",
            interval=1,
            backupCount=self.backup_count,
            encoding="utf-8"
        )

        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        self.root_logger.addHandler(file_handler)

        if self.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)  # Less verbose in console
            console_formatter = logging.Formatter(
                fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            )
            console_handler.setFormatter(console_formatter)
            self.root_logger.addHandler(console_handler)

        logging.getLogger("fastmcp").handlers.clear()


# Singleton instance for the logger
_mcp_logger: Optional[LoggerMCP] = None

def get_logger() -> LoggerMCP:
    """Get or Create & Setup Logger Instance"""
    global _mcp_logger
    if _mcp_logger is None:
        _mcp_logger = LoggerMCP()
    return _mcp_logger
