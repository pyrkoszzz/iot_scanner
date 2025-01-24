import unittest
from unittest.mock import patch
from src.modules.ipv4_scanner import IPv4Scanner


class TestIPv4Scanner(unittest.TestCase):
    @patch("src.modules.ipv4_scanner.socket.socket")
    def test_scans_single_ip_with_open_port(self, mock_socket):
        mock_socket.return_value.connect.return_value = None
        scanner = IPv4Scanner()
        result = scanner.scan_ip("192.168.0.1", [23])
        self.assertEqual(result, ("192.168.0.1", 23))

    @patch("src.modules.ipv4_scanner.logger")
    @patch("src.modules.ipv4_scanner.socket.socket")
    def test_logs_active_ip_with_open_ports(self, mock_socket, mock_logger):
        mock_socket.return_value.connect.return_value = None
        scanner = IPv4Scanner()
        result = scanner.scan_range("192.168.0.0/30", [23])
        self.assertIn("192.168.0.1", result)
        mock_logger.info.assert_any_call(
            "[+] Active IP found: 192.168.0.1 with open ports: 23"
        )
