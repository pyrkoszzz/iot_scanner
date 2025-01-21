from src.modules.input_module import InputHandler
from src.modules.credential_source import CredentialManager


def main():
    input_handler = InputHandler()
    credential_manager = CredentialManager()

    ip_ranges = input_handler.get_ip_ranges()
    credentials = credential_manager.load_credentials()

    print(ip_ranges)
    print(credentials)


if __name__ == "__main__":
    main()
