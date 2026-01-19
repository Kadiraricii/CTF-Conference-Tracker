#!/bin/bash

# setup.sh - Helper script for CTF Tracker initialization

set -e

PROJECT_ROOT="$(dirname "$(dirname "$0")")"
cd "$PROJECT_ROOT"

echo ">>> Setting up CTF Tracker..."

# 1. Check for .env
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "PLEASE EDIT .env WITH YOUR REAL CREDENTIALS!"
else
    echo ".env already exists."
fi

# 2. Docker Check
if command -v docker >/dev/null 2>&1; then
    echo "Docker found."
else
    echo "WARNING: Docker not found. You will need to run Postgres/Redis manually."
fi

# 3. Virtualenv (Optional)
read -p "Do you want to create a local python venv? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo "Created venv."
    fi
    source venv/bin/activate
    echo "Installing dependencies via pip..."
    pip install -e .
    echo "Local setup complete. Activate with: source venv/bin/activate"
fi

echo ">>> Setup finished. To start with Docker:"
echo "    docker-compose -f deploy/docker-compose.yml up --build"
