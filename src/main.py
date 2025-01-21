from src.modules.authentication import Authenticator
from src.modules.input_module import InputHandler
from src.modules.credential_source import CredentialManager
from src.modules.ipv4_scanner import IPv4Scanner


def main():
    input_handler = InputHandler()
    credential_manager = CredentialManager()
    ipv4_scanner = IPv4Scanner()
    authenticator = Authenticator()

    ip_ranges = input_handler.get_ip_ranges()
    credentials = credential_manager.load_credentials()
    open_ports = ipv4_scanner.scan(ip_ranges)
    vulnerable_devices = authenticator.authenticate(open_ports, credentials)

    print(vulnerable_devices)


if __name__ == "__main__":
    main()
