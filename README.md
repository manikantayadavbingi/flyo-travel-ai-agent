# Flyo Travel AI Agent

A travel-assistance web application built with Python and FastAPI. This project demonstrates flight search, travel expense reconciliation, REST API development, and automated testing as a foundation for a future AI-powered travel agent.

## Features

### 1. Flight Search
- Search for flights by origin, destination, and travel date.
- Filter available sample flights by budget.
- Display matching flight details, including flight number, price, and route.
- Validate search inputs and return helpful error messages.

### 2. Travel Expense Reconciliation
- Compare booking records against supplier records.
- Identify mismatches in passenger details, flight number, amount, and booking status.
- Report missing or inconsistent information.

### 3. Web Interface
- Simple browser-based interface built with HTML, CSS, and JavaScript.
- Connects to the FastAPI backend through HTTP endpoints.
- Displays flight search and reconciliation results.

### 4. Testing
- Automated unit tests for flight search and reconciliation logic.
- Input validation and mismatch detection checks.

## Tech Stack

- **Language:** Python
- **Backend:** FastAPI
- **Data validation:** Pydantic
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** Python `unittest`
- **Version control:** Git and GitHub

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
└── static/
    ├── index.html
    ├── style.css
    └── script.js
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Git
- Visual Studio Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/manikantayadavbingi/flyo-travel-ai-agent.git
cd flyo-travel-ai-agent
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks virtual environment activation, you can use Command Prompt and run:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
python -m uvicorn main:app --reload
```

### 5. Open the application

- **Web application:** http://127.0.0.1:8000/
- **Interactive API documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/api/health

Keep the terminal running while using the application. Press `Ctrl+C` to stop the server.

## Running Tests

Run the automated tests from the project root:

```bash
python -m unittest -v
```

The tests cover the flight search and reconciliation functionality.

## Current Limitations

- Flight search uses sample data and does not retrieve live airline inventory.
- Flight bookings and payments are not processed.
- Reconciliation operates on the records provided to the application.
- The application does not yet use an LLM-powered agent or external AI API.
- Authentication, persistent database storage, and production deployment are not implemented.

## Future Improvements

- Integrate a large language model (LLM) to understand travel requests in natural language.
- Build an agent workflow that can interpret user intent, validate requirements, and select appropriate tools.
- Connect to a real flight search API for live availability and pricing.
- Add database persistence for bookings and reconciliation records.
- Introduce structured logging, stronger error handling, and additional automated tests.
- Add deployment instructions and a live demo.

## Learning Objectives

This project is an opportunity to explore:

- Building REST APIs with FastAPI.
- Organizing Python code into reusable modules.
- Validating inputs and handling errors.
- Writing automated tests.
- Connecting a frontend to a backend.
- Using Git and GitHub to manage a software project.

## Disclaimer

This is an educational portfolio project. Flight information is illustrative sample data and must not be treated as real availability or a confirmed fare. The application does not make actual reservations or process payments.

---

**Author:** [manikantayadavbingi](https://github.com/manikantayadavbingi)

**Repository:** [flyo-travel-ai-agent](https://github.com/manikantayadavbingi/flyo-travel-ai-agent)
