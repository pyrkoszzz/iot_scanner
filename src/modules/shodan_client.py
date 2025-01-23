import os
from typing import Dict, Any

import shodan

from src.modules.logging_service import logger


class ShodanClient:
    def __init__(self):
        """Initializes the Shodan client with the given API key."""
        self.client = shodan.Shodan(os.environ.get("SHODAN_API_KEY"))

    def get_device_info(self, ip_address: str) -> Dict[str, Any] | None:
        """Fetches information about a device from Shodan by its IP address.

        Args:
            ip_address (str): The IP address of the device.
        """
        try:
            logger.info(f"[+] Fetching information for IP: {ip_address}")
            device_info = self.client.host(ip_address)
            return device_info
        except shodan.APIError as e:
            logger.error(f"[-] Error fetching data for {ip_address}: {e}")
            return None
