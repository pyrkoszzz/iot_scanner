import unittest
from unittest.mock import patch, mock_open
from src.modules.credential_source import CredentialManager


class TestCredentialManager(unittest.TestCase):
    @patch(
        "builtins.open", new_callable=mock_open, read_data="user1,pass1\nuser2,pass2"
    )
    @patch("csv.reader")
    def test_loads_credentials_from_default_file(self, mock_csv_reader, mock_file):
        mock_csv_reader.return_value = [["user1", "pass1"], ["user2", "pass2"]]
        manager = CredentialManager()
        credentials = manager.load_credentials()
        self.assertEqual(
            credentials, [["", ""], ["user1", "pass1"], ["user2", "pass2"]]
        )

    @patch(
        "builtins.open", new_callable=mock_open, read_data="user1,pass1\nuser2,pass2"
    )
    @patch("csv.reader")
    def test_loads_credentials_from_local_file(self, mock_csv_reader, mock_file):
        mock_csv_reader.return_value = [["user1", "pass1"], ["user2", "pass2"]]
        manager = CredentialManager(creds_directory="test/credentials")
        credentials = manager._load_local_creds()
        self.assertEqual(credentials, [["user1", "pass1"], ["user2", "pass2"]])

    @patch("builtins.open", new_callable=mock_open, read_data="")
    @patch("csv.reader")
    def test_handles_empty_credentials_file(self, mock_csv_reader, mock_file):
        mock_csv_reader.return_value = []
        manager = CredentialManager()
        credentials = manager.load_credentials()
        self.assertEqual(credentials, [["", ""]])
