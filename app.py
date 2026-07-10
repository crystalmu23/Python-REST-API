# Inventory Management System Portal

A robust Python Flask REST API backend paired with an interactive terminal CLI engine. This system allows administrators to manage inventory through full CRUD operations and fetch real-time product metadata using the OpenFoodFacts API.

## Environmental Configuration & Dependencies

This project uses `pipenv` for deterministic, locked virtual environment builds.

### Setup Instructions
```bash
# 1. Clone your repository (if running on a new machine)
# git clone <your-repo-url> && cd inventory_system

# 2. Install all required dependencies from the Pipfile
```Bash
pipenv install
```

## Running the Application Ecosystem
1. Launch the Backend REST API Server
Run this command in your first terminal window to start the microservice node:
```Bash
pipenv run python app.py
```

- The server will initialize locally at http://127.0.0.1:5000 with hot-reload Debug Mode activated.

2. Launch the Frontend Interactive CLI Console
Open a second, separate terminal window and connect to your live administrative interface dashboard:

```Bash
pipenv run python cli.py
```

## REST API Endpoints Specification
- All data transfers use standardized JSON data payloads over standard HTTP methods:

- HTTP Method	API Endpoint Path	Operational Scope Behavior	Status Codes
- GET	/inventory	Fetches the complete active inventory list	200 OK
- GET	/inventory/<id>	Extracts a single target product matching the reference ID	200 OK / 404 Not Found
- POST	/inventory	Appends a brand new item entry directly to tracking storage	201 Created / 400 Bad Request
- PATCH	/inventory/<id>	Modifies target stock counts or retail item valuation points	200 OK / 404 Not Found
- DELETE	/inventory/<id>	Permanently purges a dead product entry line from memory	200 OK / 404 Not Found
- GET	/api/external/fetch	Proxies OpenFoodFacts database via ?barcode=<number>	200 OK / 404 / 503
## Automated Testing Validation Suite
- To verify endpoint data contracts and API logic without making live external requests, a robust test suite is included using pytest and unittest.mock.

- Run the comprehensive assertion sweeps using:
```Bash
pipenv run pytest -v
```
