import json
from typing import Dict, Any


class ReportGenerator:
    """Class to generate a report of the devices found in the network scan """
    def __init__(self, report_file="reports/scan_report.json"):
        self.report_file = report_file

    def generate_report(self, devices: Dict[str, Any]):
        """
        Generates a report of the devices found in the network scan.

        Args:
            devices (dict): A dictionary of devices found in the network scan.
        """
        with open(self.report_file, "w") as file:
            json.dump(devices, file, indent=4)
