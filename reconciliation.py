
def reconcile_booking(booking, supplier_record):
    """
    Compare a booking with a supplier record.
    Report mismatches and missing fields.
    """

    fields_to_compare = [
        "passenger",
        "flight_number",
        "amount",
        "status",
    ]

    mismatches = []

    for field in fields_to_compare:
        booking_has_field = field in booking
        supplier_has_field = field in supplier_record

        booking_value = booking.get(field)
        supplier_value = supplier_record.get(field)

        # Check whether either record is missing the field.
        if not booking_has_field or not supplier_has_field:
            mismatches.append({
                "field": field,
                "issue": "missing_field",
                "booking_value": (
                    booking_value if booking_has_field else "MISSING"
                ),
                "supplier_value": (
                    supplier_value if supplier_has_field else "MISSING"
                ),
            })
            continue

        # Compare text without being sensitive to letter case
        # or accidental spaces around the text.
        if isinstance(booking_value, str) and isinstance(
            supplier_value, str
        ):
            values_match = (
                booking_value.strip().casefold()
                == supplier_value.strip().casefold()
            )
        else:
            values_match = booking_value == supplier_value

        if not values_match:
            mismatches.append({
                "field": field,
                "issue": "value_mismatch",
                "booking_value": booking_value,
                "supplier_value": supplier_value,
            })

    return {
        "booking_id": booking.get("booking_id"),
        "matched": len(mismatches) == 0,
        "mismatches": mismatches,
    }


if __name__ == "__main__":
    booking = {
        "booking_id": "BK101",
        "passenger": "Ravi Kumar",
        "flight_number": "FY101",
        "amount": 6500,
        "status": "Confirmed",
    }

    supplier_record = {
        "booking_id": "BK101",
        "passenger": "Ravi Kumar",
        "flight_number": "FY101",
        "amount": 6500,
        # Status is intentionally missing for testing.
    }

    result = reconcile_booking(booking, supplier_record)
    print(result)
