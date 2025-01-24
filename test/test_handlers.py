import logging
import unittest
from unittest.mock import patch, MagicMock
from src.modules.handlers import (
    handle_ip_scan,
    handle_telnet_open_scan,
    handle_telnet_auth_scan,
    handle_shodan_enrichment,
)

logger = logging.getLogger("IoTScanner")


class TestHandlers(unittest.TestCase):
    @patch("src.modules.ipv4_scanner.IPv4Scanner.scan_range")
    @patch.object(logger, "info", MagicMock())
    def test_scans_ip_range_for_open_ports(self, mock_scan_range):
        mock_scan_range.return_value = {"192.168.0.1": 23}
        result = handle_ip_scan("192.168.0.1/24", [23])
        self.assertEqual(result, {"192.168.0.1": 23})
        logger.info.assert_called_once_with("Scanning IP ranges for open ports...")

    @patch("src.modules.authentication.Authenticator.telnet_open_scan")
    @patch.object(logger, "info", MagicMock())
    def test_scans_for_open_telnet_devices(self, mock_telnet_open_scan):
        mock_telnet_open_scan.return_value = [("192.168.0.1", 23)]
        result = handle_telnet_open_scan({"192.168.0.1": 23})
        self.assertEqual(result, [("192.168.0.1", 23)])
        logger.info.assert_called_once_with("Scanning for open Telnet devices...")

    @patch("src.modules.authentication.Authenticator.telnet_auth_scan")
    @patch.object(logger, "info", MagicMock())
    def test_scans_for_vulnerable_telnet_devices(self, mock_telnet_auth_scan):
        mock_telnet_auth_scan.return_value = [("192.168.0.1", "admin", "password")]
        result = handle_telnet_auth_scan({"192.168.0.1": 23}, [["admin", "password"]])
        self.assertEqual(result, [("192.168.0.1", "admin", "password")])
        logger.info.assert_called_once_with("Scanning for vulnerable Telnet devices...")

    @patch("src.modules.shodan_client.ShodanClient.get_device_info")
    @patch.object(logger, "info", MagicMock())
    def test_enriches_scan_results_with_shodan_data(self, mock_get_device_info):
        mock_get_device_info.return_value = {"ip": "192.168.0.1", "data": "info"}
        result = handle_shodan_enrichment({"192.168.0.1": 23})
        self.assertEqual(result, [{"ip": "192.168.0.1", "data": "info"}])
        logger.info.assert_called_once_with(
            "Enriching scan results with Shodan data..."
        )
