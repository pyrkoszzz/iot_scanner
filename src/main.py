from modules.authentication import Authenticator
from modules.input_module import InputHandler
from modules.credential_source import CredentialManager
from modules.ipv4_scanner import IPv4Scanner
from src.modules.shodan_client import ShodanClient


def main():
    input_handler = InputHandler()
    credential_manager = CredentialManager()
    ipv4_scanner = IPv4Scanner()
    authenticator = Authenticator()
    shodan_client = ShodanClient()

    ip_ranges = input_handler.get_ip_ranges()
    credentials = credential_manager.load_credentials()
    open_ports = ipv4_scanner.scan_range(ip_ranges, [23, 2323])
    # open_telnet_devices = authenticator.telnet_open_scan(open_ports)
    # vulnerable_devices = authenticator.telnet_auth_scan(open_ports, credentials)

    print("[!] Open Telnet Devices:")
    for device in open_ports:
        device_info = shodan_client.get_device_info(device)

        if device_info:
            print("\n[Device Information]")
            print(f"IP: {device_info.get('ip_str')}")
            print(f"Organization: {device_info.get('org')}")
            print(f"ISP: {device_info.get('isp')}")
            print(f"OS: {device_info.get('os')}")
            print("Open Ports:", device_info.get("ports", []))


if __name__ == "__main__":
    main()
