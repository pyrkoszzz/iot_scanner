import unittest
from src.iot_modules.cli_parser import CLIParser


class TestCLIParser(unittest.TestCase):
    def test_parses_scan_ips_argument(self):
        parser = CLIParser.get_parser()
        args = parser.parse_args(["--scan-ips"])
        self.assertTrue(args.scan_ips)

    def test_parses_scan_telnet_open_argument(self):
        parser = CLIParser.get_parser()
        args = parser.parse_args(["--scan-telnet-open"])
        self.assertTrue(args.scan_telnet_open)

    def test_parses_scan_telnet_auth_argument(self):
        parser = CLIParser.get_parser()
        args = parser.parse_args(["--scan-telnet-auth"])
        self.assertTrue(args.scan_telnet_auth)

    def test_parses_ports_argument(self):
        parser = CLIParser.get_parser()
        args = parser.parse_args(["--ports", "22", "80"])
        self.assertEqual(args.ports, [22, 80])

    def test_parses_ip_range_argument(self):
        parser = CLIParser.get_parser()
        args = parser.parse_args(["--ip-range", "192.168.0.1/24"])
        self.assertEqual(args.ip_range, "192.168.0.1/24")

    def test_parses_credentials_argument(self):
        parser = CLIParser.get_parser()
        args = parser.parse_args(["--credentials", "path/to/credentials.txt"])
        self.assertEqual(args.credentials, "path/to/credentials.txt")

    def test_parses_shodan_enrichment_argument(self):
        parser = CLIParser.get_parser()
        args = parser.parse_args(["--shodan-enrichment"])
        self.assertTrue(args.shodan_enrichment)

    def test_uses_default_ports(self):
        parser = CLIParser.get_parser()
        args = parser.parse_args([])
        self.assertEqual(args.ports, [23, 2323])
