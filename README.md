
# Flyo Travel Agent

A web-based travel operations prototype built with Python, FastAPI, HTML, CSS, and JavaScript.

The application demonstrates flight search and booking reconciliation workflows that can help automate repetitive travel operations tasks.

## Features

### 1. Flight Search
- Search flights by origin and destination.
- Filter results by travel date.
- Apply an optional maximum budget.
- Validate search inputs.
- Display matching sample flight results.

### 2. Booking Reconciliation
- Compare booking records with supplier records.
- Check passenger names, flight numbers, amounts, and booking statuses.
- Detect missing fields and value mismatches.
- Display reconciliation results through the website.

### 3. Backend API
- FastAPI endpoints for flight search and reconciliation.
- Pydantic request validation.
- Error handling for invalid requests.
- Health-check endpoint.

### 4. Automated Tests
- Unit tests for flight search.
- Unit tests for booking reconciliation.
- Validation of successful matches and mismatch scenarios.

## Technology Stack

- **Python** — business logic and data processing
- **FastAPI** — backend API framework
- **Pydantic** — request validation
- **HTML** — webpage structure
- **CSS** — styling and responsive layout
- **JavaScript** — frontend interactions and API requests
- **Uvicorn** — local development server
- **unittest** — automated testing

## Project Structure

```text
flyo-travel-ai-agent/
├── main.py
├── flight_search.py
├── reconciliation.py
├── test_flight_search.py
├── test_reconciliation.py
├── requirements.txt
├── README.md
├── .gitignore
└── static/
    ├── index.html
    ├── style.css
    └── script.js
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- pip

### Installation

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Navigate to the project directory:

   ```bash
   cd flyo-travel-ai-agent
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment.

   **Windows PowerShell:**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

### Run the Application

Start the development server:

```bash
python -m uvicorn main:app --reload
```

Open these addresses in your browser:

- Website: http://127.0.0.1:8000/
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/health

### Run Tests

Run the automated tests with:

```bash
python -m unittest -v
```

## Important Limitations

- Flight search uses fictional sample data, not live airline inventory.
- The application does not currently book or ticket real flights.
- Booking reconciliation operates on records supplied to the application.
- An LLM-based AI agent and live supplier integrations are planned future improvements.

## Future Improvements

- Integrate a legitimate flight-data provider.
- Add an LLM-based assistant with controlled tool calling.
- Store booking and reconciliation history in a database.
- Add authentication and role-based access control.
- Deploy the application to a hosted environment.

## Project Goal

This project demonstrates foundational skills in backend API development, frontend integration, input validation, business logic, and automated testing, with a focus on travel operations automation.
