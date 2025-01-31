import logging
import unittest
from unittest.mock import patch, MagicMock
from src.iot_modules.logging_service import LoggingService


class TestLoggingService(unittest.TestCase):
    @patch("os.makedirs")
    @patch("logging.getLogger")
    def test_initializes_logging_service_with_default_values(
        self, mock_get_logger, mock_makedirs
    ):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        service = LoggingService()
        self.assertEqual(service.log_file, "logs/scan_logs.log")
        self.assertEqual(service.log_level, logging.INFO)
        self.assertEqual(service.max_bytes, 5 * 1024 * 1024)
        self.assertEqual(service.backup_count, 3)
        mock_makedirs.assert_called_once_with("logs", exist_ok=True)
        mock_get_logger.assert_called_once_with("IoTScanner")

    @patch("os.makedirs")
    @patch("logging.getLogger")
    def test_initializes_logging_service_with_custom_values(
        self, mock_get_logger, mock_makedirs
    ):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        service = LoggingService(
            log_file="custom.log",
            log_level=logging.DEBUG,
            max_bytes=1024,
            backup_count=1,
        )
        self.assertEqual(service.log_file, "custom.log")
        self.assertEqual(service.log_level, logging.DEBUG)
        self.assertEqual(service.max_bytes, 1024)
        self.assertEqual(service.backup_count, 1)
        mock_makedirs.assert_called_once_with("", exist_ok=True)
        mock_get_logger.assert_called_once_with("IoTScanner")

    @patch("logging.getLogger")
    def test_returns_configured_logger_instance(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        service = LoggingService()
        logger = service.get_logger()
        self.assertEqual(logger, mock_logger)

    @patch("logging.getLogger")
    def configures_handlers_only_once(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        service = LoggingService()
        service._configure_handlers = MagicMock()
        service._configure_handlers()
        service._configure_handlers.assert_called_once()
