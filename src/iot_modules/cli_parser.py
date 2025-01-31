import argparse


class CLIParser:
    """CLI argument parser for the network scanning tool."""

    @staticmethod
    def get_parser():
        """Returns the CLI argument parser."""
        parser = argparse.ArgumentParser(
            description="CLI for network scanning and authentication handling."
        )

        parser.add_argument(
            "--scan-ips", action="store_true", help="Scan IP ranges for open ports."
        )
        parser.add_argument(
            "--scan-telnet-open",
            action="store_true",
            help="Scan for open Telnet devices.",
        )
        parser.add_argument(
            "--scan-telnet-auth",
            action="store_true",
            help="Perform Telnet authentication scan to find vulnerable devices.",
        )
        parser.add_argument(
            "--ports",
            type=int,
            nargs="+",
            default=[23, 2323],
            help="Ports to scan (default: 23, 2323).",
        )
        parser.add_argument(
            "--ip-range",
            type=str,
            help="IP ranges to scan (e.g., 192.168.0.1/24).",
        )
        parser.add_argument(
            "--credentials",
            type=str,
            help="Path to the credentials file for authentication scans.",
        )

        parser.add_argument(
            "--shodan-enrichment",
            action="store_true",
            help="Enrich scan results with Shodan data.",
        )

        parser.add_argument(
            "--report-file",
            type=str,
            default="reports/scan_report.json",
            help="Path to the report file (default: reports/scan_report.json).",
        )

        return parser
