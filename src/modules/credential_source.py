import csv


class CredentialManager:
    def __init__(self, creds_directory="config/credentials"):
        self.creds_directory = creds_directory

    def load_credentials(self):
        credentials = [["", ""]]
        credentials += self._load_local_creds()
        return credentials

    def _load_local_creds(self):
        filepath = f"{self.creds_directory}/default_creds.csv"
        with open(filepath, "r") as file:
            return [line for line in csv.reader(file)]
