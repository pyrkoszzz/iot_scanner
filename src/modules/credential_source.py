import csv

from src.modules.logging_service import logger


class CredentialManager:
    """
    A class to manage credentials for the IoT scanner.
    """

    def __init__(self, creds_directory="config/credentials"):
        self.creds_directory = creds_directory

    def load_credentials(self):
        """
        Load credentials from the default file and the local file.

        Returns:
            list: A list of credentials
        """
        credentials = [["", ""]]
        credentials += self._load_local_creds()
        logger.info(f"Loaded {len(credentials) - 1} credentials.")
        return credentials

    def _load_local_creds(self):
        """
        Load credentials from the local file.

        Returns:
            list: A list of credentials
        """
        logger.debug("Loading credentials from the local file.")
        filepath = f"{self.creds_directory}/default_creds.csv"
        with open(filepath, "r") as file:
            return [line for line in csv.reader(file)]
