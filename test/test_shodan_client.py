import logging
import unittest
from unittest.mock import patch, MagicMock

import shodan

from src.iot_modules.shodan_client import ShodanClient

logger = logging.getLogger("IoTScanner")


class TestShodanClient(unittest.TestCase):
    @patch("shodan.Shodan.host")
    @patch.object(logger, "info", MagicMock())
    def test_fetches_device_info_successfully(self, mock_host):
        mock_host.return_value = {"ip": "192.168.0.1", "data": "info"}
        client = ShodanClient()
        result = client.get_device_info("192.168.0.1")
        self.assertEqual(result, {"ip": "192.168.0.1", "data": "info"})
        logger.info.assert_called_once_with(
            "[+] Fetching information for IP: 192.168.0.1"
        )

    @patch("shodan.Shodan.host")
    @patch.object(logger, "error", MagicMock())
    def test_handles_api_error_gracefully(self, mock_host):
        mock_host.side_effect = shodan.APIError("API error")
        client = ShodanClient()
        result = client.get_device_info("192.168.0.1")
        self.assertIsNone(result)
        logger.error.assert_called_once_with(
            "[-] Error fetching data for 192.168.0.1: API error"
        )
