# ML Project FastAPI — Setup Guide

This document describes all steps required to install dependencies and start the FastAPI server, making the Swagger UI available at **http://localhost:8002/docs**.

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10 or higher (project uses 3.13) |
| pip | latest recommended |
| OS | Windows (PowerShell), Linux, or macOS |

Verify your Python version before starting:

```powershell
python --version
```


---

## Project Structure (relevant parts)

```
ml_project/
├── data/
│   └── dataset.csv          # Training data (required at startup)
├── src/
│   ├── app/
│   │   ├── main.py          # FastAPI app factory
│   │   └── api/
│   │       └── loan_processing.py
│   └── ml_project/
│       ├── components/
│       │   └── data_processing.py
│       ├── entity/
│       │   └── config_entity.py
│       └── pipeline/
│           └── prediction.py
├── requirements.txt
└── setup.py
```

---

## Step 1 — Clone / Navigate to the Project

Open a terminal (PowerShell on Windows) and navigate to the project root:

```powershell
cd c:\Users\Dell\.gemini\antigravity\scratch\ml_project
```

---

## Step 2 — Create a Virtual Environment

Create a dedicated Python virtual environment to isolate dependencies:

```powershell
python -m venv venv
```

---

## Step 3 — Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

> After activation your terminal prompt will be prefixed with `(venv)`.

---

## Step 4 — Install the Package in Editable Mode

This registers the `src/` package so all internal imports resolve correctly:

```powershell
pip install -e .
```

---

## Step 5 — Install All Dependencies

```powershell
pip install -r requirements.txt
```

### What gets installed

| Package | Purpose |
|---|---|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `pydantic` | Request/response validation |
| `scikit-learn` | ML model & preprocessing |
| `pandas` | Data loading and manipulation |
| `numpy` | Numerical operations |
| `pytest` | (dev) Testing |
| `requests` | (dev) HTTP client for tests |
| `nest-asyncio` | Async compatibility |

---

## Step 6 — Verify the Dataset is Present

The server trains a logistic regression model on startup using `data/dataset.csv`. Confirm the file exists:

```powershell
Test-Path data\dataset.csv
```

Expected output: `True`

If missing, place the `dataset.csv` file in the `data/` directory before starting the server.

---

## Step 7 — Start the Server

Run the following command from the project root:

```powershell
venv\Scripts\python.exe -m uvicorn src.app.main:app --host 0.0.0.0 --port 8002 --reload
```

### What the flags do

| Flag | Description |
|---|---|
| `--host 0.0.0.0` | Accept connections from any network interface |
| `--port 8002` | Listen on port 8002 |
| `--reload` | Auto-reload on code changes (development mode) |

### Expected startup output

```
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://0.0.0.0:8002 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

> **Note:** The first startup may take 10–20 seconds while the model trains on `dataset.csv`.

---

## Step 8 — Open the Swagger UI

Once the server is running, open your browser and navigate to:

```
http://localhost:8002/docs
```

You will see the interactive **ML Project FastAPI** Swagger UI with the available endpoints.

---

## Available Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/process_loan_applications` | Submit one or more loan applications for ML inference |
| `GET` | `/ping` | Health check — returns `{"ping": "pong!"}` |

---

## Example Payload — `POST /process_loan_applications`

Send a JSON array of loan applications. All fields are optional (missing fields use training-set medians):

```json
[
  {
    "Annual_Income": 75000,
    "Monthly_Expenses": 2000,
    "Dependents": 2,
    "FICO_Score": 720,
    "Debt_to_Income_Ratio": 0.3,
    "Credit_Utilization": 0.25
  }
]
```

### Example Response

```json
{
  "status": "success",
  "processed_count": 1,
  "results": [
    {
      "application_index": 0,
      "prediction": "Approved"
    }
  ]
}
```

---

## Stopping the Server

Press **CTRL + C** in the terminal where the server is running.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'src'` | Run `pip install -e .` from the project root |
| `Dataset not found` warning on startup | Ensure `data/dataset.csv` exists |
| Port 8002 already in use | Change `--port 8002` to another port (e.g. `8003`) |
| `Activate.ps1 cannot be loaded` (PowerShell policy) | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` first |
| Slow first startup | Normal — model training on `dataset.csv` happens at server boot |
