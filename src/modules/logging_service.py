import logging
from logging.handlers import RotatingFileHandler
import os


class LoggingService:
    """
    A centralized logging service for the IoT scanner.
    Provides logging utilities for various modules and handles
    file rotation, formatting, and log level configuration.
    """

    def __init__(
        self,
        log_file="logs/scan_logs.log",
        log_level=logging.INFO,
        max_bytes=5 * 1024 * 1024,
        backup_count=3,
    ):
        """
        Initializes the logging service.

        Args:
            log_file (str): The path to the log file.
            log_level (int): The logging level.
            max_bytes (int): The maximum size of the log file in bytes.
            backup_count (int): The number of backup logs to keep.
        """
        self.log_file = log_file
        self.log_level = log_level
        self.max_bytes = max_bytes
        self.backup_count = backup_count

        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        self.logger = logging.getLogger("IoTScanner")
        self.logger.setLevel(self.log_level)

        if not self.logger.hasHandlers():
            self._configure_handlers()

    def _configure_handlers(self):
        """
        Configure the logging handlers and formatters.
        """
        file_handler = RotatingFileHandler(
            self.log_file, maxBytes=self.max_bytes, backupCount=self.backup_count
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self._get_formatter())

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(self._get_formatter())

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    @staticmethod
    def _get_formatter():
        """
        Returns a standard log formatter.

        Returns:
             A logging formatter instance.
        """
        return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def get_logger(self):
        """
        Returns the configured logger instance.

        Returns:
            A logger instance.
        """
        return self.logger


logger = LoggingService().get_logger()
