
import json
import tempfile
import unittest
from pathlib import Path

from weekly_report import generate_report


class TestWeeklyReport(unittest.TestCase):

    def test_calculates_total_spending(self):
        report = generate_report(
            {"EC2": 2.00, "S3": 1.00},
            {"EC2": 3.00, "S3": 1.50}
        )

        self.assertEqual(report["previous_period_total"], 3.00)
        self.assertEqual(report["current_period_total"], 4.50)
        self.assertEqual(report["total_difference"], 1.50)

    def test_flags_large_increase(self):
        report = generate_report(
            {"EC2": 2.00},
            {"EC2": 3.50}
        )

        self.assertEqual(
            report["services"][0]["status"],
            "investigate_increase"
        )

    def test_detects_new_service(self):
        report = generate_report(
            {},
            {"Lambda": 0.80}
        )

        self.assertEqual(
            report["services"][0]["status"],
            "investigate_increase"
        )

    def test_detects_decrease(self):
        report = generate_report(
            {"S3": 1.00},
            {"S3": 0.50}
        )

        self.assertEqual(
            report["services"][0]["status"],
            "decreased"
        )

    def test_report_contains_required_fields(self):
        report = generate_report(
            {"EC2": 2.00},
            {"EC2": 3.00}
        )

        self.assertIn("report_date", report)
        self.assertIn("currency", report)
        self.assertIn("previous_period_total", report)
        self.assertIn("current_period_total", report)
        self.assertIn("total_difference", report)
        self.assertIn("services", report)

        self.assertEqual(report["currency"], "USD")

    def test_json_report_can_be_saved_and_read(self):
        report = generate_report(
            {"EC2": 2.00},
            {"EC2": 3.00}
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "weekly_report.json"

            with report_path.open("w", encoding="utf-8") as file:
                json.dump(report, file, indent=2)

            with report_path.open("r", encoding="utf-8") as file:
                loaded_report = json.load(file)

        self.assertEqual(
            loaded_report["current_period_total"],
            3.00
        )
        self.assertEqual(loaded_report["services"][0]["service"], "EC2")


if __name__ == "__main__":
    unittest.main()
