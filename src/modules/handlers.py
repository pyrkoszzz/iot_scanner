from typing import Dict, Tuple, List

from src.modules.authentication import Authenticator
from src.modules.ipv4_scanner import IPv4Scanner
from src.modules.logging_service import logger
from src.modules.shodan_client import ShodanClient


def handle_ip_scan(ip_range: str, ports: int) -> Dict[str, int]:
    """
    Scans IP ranges for open ports.

    Args:
        ip_range (str): The IP range to scan.
        ports (int): The ports to scan.

    Returns:
        list: A list of open ports.
    """
    logger.info("Scanning IP ranges for open ports...")
    ipv4_scanner = IPv4Scanner()
    open_ports = ipv4_scanner.scan_range(ip_range, ports)
    return open_ports


def handle_telnet_open_scan(open_ports: Dict[str, int]) -> List[Tuple[str, int]]:
    """
    Scans for open Telnet devices.

    Args:
        open_ports (dict): A list of open ports.

    Returns:
        list: A list of open Telnet devices.
    """
    logger.info("Scanning for open Telnet devices...")
    authenticator = Authenticator()
    open_telnet_devices = authenticator.telnet_open_scan(open_ports)
    return open_telnet_devices


def handle_telnet_auth_scan(open_ports: Dict[str, int], credentials: List[List[str]]) -> List[Tuple[str, str, str]]:
    """
    Performs Telnet authentication scan to find vulnerable devices.

    Args:
        open_ports (dict): A list of open ports.
        credentials (list): A list of username/password combinations.

    Returns:
        list: A list of vulnerable Telnet devices.
    """
    logger.info("Scanning for vulnerable Telnet devices...")
    authenticator = Authenticator()
    vulnerable_devices = authenticator.telnet_auth_scan(open_ports, credentials)
    return vulnerable_devices


def handle_shodan_enrichment(open_ports: Dict[str, int]) -> List[Dict[str, str]]:
    """
    Enriches scan results with Shodan data.

    Args:
        open_ports (dict): A list of open ports.

    Returns:
        list: A list of Shodan-enriched device information.
    """
    logger.info("Enriching scan results with Shodan data...")
    shodan_client = ShodanClient()
    shodan_results = []
    for ip in open_ports:
        shodan_results.append(shodan_client.get_device_info(ip))
    return shodan_results
