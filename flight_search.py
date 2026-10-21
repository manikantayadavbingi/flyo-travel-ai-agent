
from datetime import date

# Sample data only — these are fictional flights, not live offers.
FLIGHTS = [
    {
        "flight_number": "FY101",
        "airline": "Demo Air",
        "origin": "HYD",
        "destination": "DEL",
        "date": "2026-10-30",
        "price": 6500,
        "departure": "08:30",
    },
    {
        "flight_number": "FY102",
        "airline": "Demo Air",
        "origin": "HYD",
        "destination": "DEL",
        "date": "2026-10-30",
        "price": 9200,
        "departure": "14:15",
    },
    {
        "flight_number": "FY203",
        "airline": "Sample Wings",
        "origin": "HYD",
        "destination": "BLR",
        "date": "2026-10-30",
        "price": 4800,
        "departure": "10:00",
    },
    {
        "flight_number": "FY104",
        "airline": "Demo Air",
        "origin": "HYD",
        "destination": "DEL",
        "date": "2026-10-31",
        "price": 7200,
        "departure": "09:00",
    },
]


def search_flights(origin, destination, travel_date, max_price=None):
    """Search sample flights using route, date, and optional budget."""

    origin = origin.strip().upper()
    destination = destination.strip().upper()

    # Validate airport codes.
    if len(origin) != 3 or not origin.isalpha():
        raise ValueError("Origin must be a three-letter airport code.")

    if len(destination) != 3 or not destination.isalpha():
        raise ValueError("Destination must be a three-letter airport code.")

    # Validate the date format and calendar date.
    try:
        parsed_date = date.fromisoformat(travel_date)
    except (ValueError, TypeError):
        raise ValueError("Date must use YYYY-MM-DD format.")

    if parsed_date < date.today():
        raise ValueError("Travel date cannot be in the past.")

    if origin == destination:
        raise ValueError("Origin and destination must be different.")

    if max_price is not None:
        if isinstance(max_price, bool) or not isinstance(max_price, (int, float)):
            raise ValueError("Budget must be a number.")

        if max_price < 0:
            raise ValueError("Budget cannot be negative.")

    results = []

    for flight in FLIGHTS:
        matches_route = (
            flight["origin"] == origin
            and flight["destination"] == destination
        )
        matches_date = flight["date"] == travel_date
        matches_budget = (
            max_price is None or flight["price"] <= max_price
        )

        if matches_route and matches_date and matches_budget:
            results.append(flight)

    # Show the cheapest matching flight first.
    results.sort(key=lambda flight: flight["price"])

    return results


if __name__ == "__main__":
    flights = search_flights(
        origin="HYD",
        destination="DEL",
        travel_date="2026-10-30",
        max_price=8000,
    )

    if flights:
        for flight in flights:
            print(
                f'{flight["flight_number"]} | '
                f'{flight["origin"]} → {flight["destination"]} | '
                f'₹{flight["price"]} | '
                f'{flight["departure"]}'
            )
    else:
        print("No matching flights found.")
