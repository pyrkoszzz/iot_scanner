import unittest
from unittest.mock import patch, mock_open
from src.iot_modules.report_generator import ReportGenerator


class TestReportGenerator(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_generates_report_with_devices(self, mock_json_dump, mock_file):
        devices = {"192.168.0.1": {"device": "Router"}}
        generator = ReportGenerator()
        generator.generate_report(devices)
        mock_file.assert_called_once_with("reports/scan_report.json", "w")
        mock_json_dump.assert_called_once_with(devices, mock_file(), indent=4)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_generates_report_with_empty_devices(self, mock_json_dump, mock_file):
        devices = {}
        generator = ReportGenerator()
        generator.generate_report(devices)
        mock_file.assert_called_once_with("reports/scan_report.json", "w")
        mock_json_dump.assert_called_once_with(devices, mock_file(), indent=4)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_generates_report_with_custom_file(self, mock_json_dump, mock_file):
        devices = {"192.168.0.1": {"device": "Router"}}
        generator = ReportGenerator(report_file="custom_report.json")
        generator.generate_report(devices)
        mock_file.assert_called_once_with("custom_report.json", "w")
        mock_json_dump.assert_called_once_with(devices, mock_file(), indent=4)
