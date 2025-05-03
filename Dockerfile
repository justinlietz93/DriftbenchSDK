# Use the official Python image.
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# Using requirements.txt instead of pip install "driftbench[prod]" for scaffold
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# --- Placeholder for Roslyn Daemon Build ---
# The blueprint requires building the C# Roslyn daemon.
# This typically requires the .NET SDK in the build environment.
# For this scaffold, we are skipping the actual build.
# You would need a multi-stage build or install .NET SDK here.
# Example (requires .NET SDK installed):
# WORKDIR /app/roslyn_daemon
# RUN dotnet publish -c Release -o /roslyn
# WORKDIR /app
# -------------------------------------------

# Expose the port the app runs on (Gunicorn default is 8000 if not specified)
# Flask app in api.py is set to run on 8000 for dev, Gunicorn will use it too
EXPOSE 8000

# Define the command to run the application using Gunicorn
# Matches the blueprint specification
CMD ["gunicorn", "sdk.api:app", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "-w", "2"]

