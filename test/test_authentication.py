import unittest
from unittest.mock import patch
from src.modules.authentication import Authenticator


class TestAuthenticator(unittest.TestCase):
    @patch("telnetlib.Telnet")
    @patch("src.modules.logging_service.logger")
    def test_detects_open_telnet_successfully(self, mock_logger, mock_telnet):
        mock_telnet.return_value.read_until.return_value = b"0\n"
        result = Authenticator.detect_open_telnet("192.168.0.1", 23)
        self.assertEqual(result, ("192.168.0.1", 23))

    @patch("telnetlib.Telnet")
    @patch("src.modules.logging_service.logger")
    def test_detects_open_telnet_failure(self, mock_logger, mock_telnet):
        mock_telnet.side_effect = Exception("Connection failed")
        result = Authenticator.detect_open_telnet("192.168.0.1", 23)
        self.assertIsNone(result)
        mock_logger.info.assert_not_called()

    @patch("telnetlib.Telnet")
    @patch("src.modules.logging_service.logger")
    def test_attempts_telnet_auth_failure(self, mock_logger, mock_telnet):
        mock_telnet.side_effect = Exception("Authentication failed")
        result = Authenticator.attempt_telnet_auth(
            "192.168.0.1", 23, "admin", "password"
        )
        self.assertIsNone(result)
        mock_logger.info.assert_not_called()

    @patch("src.modules.authentication.Authenticator.detect_open_telnet")
    def test_scans_for_open_telnet_servers(self, mock_detect_open_telnet):
        mock_detect_open_telnet.return_value = ("192.168.0.1", 23)
        authenticator = Authenticator()
        result = authenticator.telnet_open_scan({"192.168.0.1": 23})
        self.assertEqual(result, [("192.168.0.1", 23)])
        mock_detect_open_telnet.assert_called_once_with("192.168.0.1", 23)

    @patch("src.modules.authentication.Authenticator.attempt_telnet_auth")
    def test_scans_for_telnet_authentication(self, mock_attempt_telnet_auth):
        mock_attempt_telnet_auth.return_value = ("192.168.0.1", "admin", "password")
        authenticator = Authenticator()
        result = authenticator.telnet_auth_scan(
            {"192.168.0.1": 23}, [["admin", "password"]]
        )
        self.assertEqual(result, [("192.168.0.1", "admin", "password")])
        mock_attempt_telnet_auth.assert_called_once_with(
            "192.168.0.1", 23, "admin", "password"
        )
