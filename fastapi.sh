#!/bin/bash

# Navigate to project directory
cd /home/ubuntu/Foodie-Ecosystem

# Load Poetry environment (ensure it's in PATH)
export PATH="$HOME/.local/bin:$PATH"

# Run your FastAPI app with poetry
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
