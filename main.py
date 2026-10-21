
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from flight_search import search_flights
from reconciliation import reconcile_booking


# ---------- Paths ----------

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


# ---------- FastAPI Application ----------

app = FastAPI(
    title="Flyo Travel Agent",
    description=(
        "A travel operations demo with flight search "
        "and booking reconciliation."
    ),
    version="1.0.0",
)


# ---------- Frontend Static Files ----------

if not STATIC_DIR.is_dir():
    raise RuntimeError(
        f"Frontend folder not found: {STATIC_DIR}"
    )

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


# ---------- Request Models ----------

class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    travel_date: date
    max_price: float | None = None


class ReconciliationRequest(BaseModel):
    booking: dict
    supplier_record: dict


# ---------- Website Home Page ----------

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


# ---------- Health Check ----------

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "Flyo Travel Agent API is running.",
    }


# ---------- Flight Search API ----------

@app.post("/flights/search")
def find_flights(request: FlightSearchRequest):
    try:
        flights = search_flights(
            origin=request.origin,
            destination=request.destination,
            travel_date=request.travel_date.isoformat(),
            max_price=request.max_price,
        )

        return {
            "count": len(flights),
            "flights": flights,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


# ---------- Booking Reconciliation API ----------

@app.post("/reconciliation/check")
def check_reconciliation(
    request: ReconciliationRequest,
):
    try:
        result = reconcile_booking(
            request.booking,
            request.supplier_record,
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
