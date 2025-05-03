# DriftBench SDK (Scaffold)

This repository contains the initial project scaffold for the DriftBench SDK, generated based on the technical blueprint.

DriftBench is intended as middleware that guarantees every LLM response is syntactically correct, semantically valid, standards-compliant, and on-topic before reaching the user.

**Note:** This is a scaffold project. Most components contain placeholder logic and `TODO` comments indicating where implementation is needed.

## Project Structure

```
root/
├─ sdk/              # Core SDK logic
│  ├─ validators/     # Validator implementations
│  ├─ api.py          # Flask API endpoint
│  ├─ orchestrator.py # Validation orchestrator (TODO)
│  ├─ replanner.py    # LLM replanning logic (TODO)
│  ├─ logger_async.py # Async SQLite logger
│  └─ ...
├─ roslyn_daemon/    # C# AST gRPC service (Stub)
├─ cli/              # Command-line interface
│  └─ main.py
├─ tests/            # Pytest tests (basic smoke test included)
├─ k8s/              # Kubernetes manifests (TODO: review/complete)
│  ├─ deployment.yaml
│  └─ config-map.yaml
├─ standards.json    # Rule configuration
├─ Dockerfile        # Container definition
├─ setup.py          # Package setup
├─ requirements.txt  # Python dependencies
└─ README.md         # This file
```

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd driftbench_sdk
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```bash
    python3.9 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install the package in editable mode with development dependencies:**
    ```bash
    pip install -e .[dev]
    ```
    This command installs the necessary packages defined in `setup.py` and `requirements.txt`, including Flask, Gunicorn, Click, and pytest.

> **Windows PowerShell**  
> Use quotes around the extras spec:  
> `pip install -e ".[dev]"`  
> Gunicorn is not installed on Windows; run the API with `uvicorn sdk.api:app`.

## Basic Usage

### Run the API Server

The API server provides endpoints for health checks and response filtering.

```bash
driftbench serve
```

This command (currently a stub) is intended to start the Flask application using Gunicorn. For development, you can also run the Flask app directly:

```bash
python sdk/api.py
```

The API will be available at `http://localhost:8000`.

- `/health` (GET): Returns `{"status": "healthy"}`.
- `/filter` (POST): Expects `{"prompt": "...", "response": "..."}` JSON. Returns a stub response.

### Other CLI Commands (Stubs)

The following CLI commands are registered but currently only print `TODO` messages:

- `driftbench watch`: Intended for live drift monitoring.
- `driftbench calibrate`: Intended for rule calibration.
- `driftbench export`: Intended for exporting log data.

## Development

- **Run tests:**
  ```bash
  pytest
  ```
- **Implement TODOs:** Fill in the logic in the various Python and C# files as indicated by `TODO` comments.
- **Roslyn Daemon:** The `roslyn_daemon` requires the .NET SDK to build and run. The `Dockerfile` and `Program.cs` contain placeholders for this.
- **Configuration:** Modify rules and settings in `standards.json`.

## Next Steps

Refer to the original technical blueprint and the `TODO` comments within the code to continue development.
