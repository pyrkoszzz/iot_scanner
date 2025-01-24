from src.modules.cli_parser import CLIParser
from src.modules.credential_source import CredentialManager
from src.modules.handlers import (
    handle_ip_scan,
    handle_telnet_open_scan,
    handle_telnet_auth_scan,
    handle_shodan_enrichment,
)
from src.modules.logging_service import logger


def main():
    parser = CLIParser.get_parser()
    args = parser.parse_args()

    credential_manager = CredentialManager()

    ip_ranges = args.ip_range
    credentials = None
    open_ports = []

    if args.credentials:
        credentials = credential_manager.load_credentials()

    if args.scan_ips:
        open_ports = handle_ip_scan(ip_ranges, args.ports)

    elif args.scan_telnet_open:
        open_ports = handle_ip_scan(ip_ranges, args.ports)
        handle_telnet_open_scan(open_ports)

    elif args.scan_telnet_auth:
        if not credentials:
            logger.error("Credentials file is required for Telnet authentication scan.")
            return
        open_ports = handle_ip_scan(ip_ranges, args.ports)
        handle_telnet_auth_scan(open_ports, credentials)

    if args.shodan_enrichment and open_ports:
        handle_shodan_enrichment(open_ports)


if __name__ == "__main__":
    main()
