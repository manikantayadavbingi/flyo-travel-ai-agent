
import unittest

from reconciliation import reconcile_booking


class TestReconciliation(unittest.TestCase):

    def setUp(self):
        self.booking = {
            "booking_id": "BK101",
            "passenger": "Ravi Kumar",
            "flight_number": "FY101",
            "amount": 6500,
            "status": "confirmed",
        }

        self.supplier_record = self.booking.copy()

    def test_matching_records(self):
        result = reconcile_booking(
            self.booking, self.supplier_record
        )

        self.assertTrue(result["matched"])
        self.assertEqual(result["mismatches"], [])

    def test_amount_mismatch(self):
        self.supplier_record["amount"] = 7000

        result = reconcile_booking(
            self.booking, self.supplier_record
        )

        self.assertFalse(result["matched"])
        self.assertEqual(
            result["mismatches"][0]["field"], "amount"
        )
        self.assertEqual(
            result["mismatches"][0]["issue"], "value_mismatch"
        )

    def test_flight_number_mismatch(self):
        self.supplier_record["flight_number"] = "FY202"

        result = reconcile_booking(
            self.booking, self.supplier_record
        )

        self.assertFalse(result["matched"])
        self.assertEqual(
            result["mismatches"][0]["field"], "flight_number"
        )

    def test_missing_passenger_field(self):
        del self.supplier_record["passenger"]

        result = reconcile_booking(
            self.booking, self.supplier_record
        )

        self.assertFalse(result["matched"])
        self.assertEqual(
            result["mismatches"][0]["issue"], "missing_field"
        )
        self.assertEqual(
            result["mismatches"][0]["supplier_value"], "MISSING"
        )

    def test_text_comparison_ignores_case_and_spaces(self):
        self.supplier_record["status"] = "  CONFIRMED  "

        result = reconcile_booking(
            self.booking, self.supplier_record
        )

        self.assertTrue(result["matched"])

    def test_detects_multiple_mismatches(self):
        self.supplier_record["flight_number"] = "FY202"
        self.supplier_record["amount"] = 7000

        result = reconcile_booking(
            self.booking, self.supplier_record
        )

        self.assertFalse(result["matched"])
        self.assertEqual(len(result["mismatches"]), 2)


if __name__ == "__main__":
    unittest.main()
