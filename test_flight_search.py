
import unittest
from flight_search import search_flights


class TestFlightSearch(unittest.TestCase):

    def test_finds_flights_within_budget(self):
        results = search_flights(
            "HYD", "DEL", "2026-10-30", 8000
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["flight_number"], "FY101")

    def test_returns_no_results_for_wrong_route(self):
        results = search_flights(
            "BLR", "DEL", "2026-10-30"
        )
        self.assertEqual(results, [])

    def test_sorts_results_by_price(self):
        results = search_flights(
            "HYD", "DEL", "2026-10-30"
        )
        prices = [flight["price"] for flight in results]
        self.assertEqual(prices, sorted(prices))

    def test_rejects_invalid_date(self):
        with self.assertRaises(ValueError):
            search_flights("HYD", "DEL", "30-10-2026")

    def test_rejects_same_origin_and_destination(self):
        with self.assertRaises(ValueError):
            search_flights("HYD", "HYD", "2026-10-30")

    def test_rejects_negative_budget(self):
        with self.assertRaises(ValueError):
            search_flights("HYD", "DEL", "2026-10-30", -100)


if __name__ == "__main__":
    unittest.main()
