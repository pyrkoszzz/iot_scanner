import os
import shodan


class ShodanClient:
    def __init__(self):
        """Initializes the Shodan client with the given API key."""
        self.client = shodan.Shodan(os.environ.get("SHODAN_KEY"))

    def get_device_info(self, ip_address):
        """Fetches information about a device from Shodan by its IP address."""
        try:
            print(f"[+] Fetching information for IP: {ip_address}")
            device_info = self.client.host(ip_address)
            return device_info
        except shodan.APIError as e:
            print(f"[-] Error fetching data for {ip_address}: {e}")
            return None
