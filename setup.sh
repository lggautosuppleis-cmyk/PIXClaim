#!/usr/bin/env bash
set -e
echo "Setup script: prepare environment"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Environment ready. Use 'scripts/start.sh' to run docker compose."
