#!/usr/bin/env bash
set -euo pipefail

# Create a virtual environment for running the analyzer
echo "Starting virtual environment..."
python3 -m venv venv >/dev/null 2>&1
source venv/bin/activate

echo "Downloading packages..."
pip install -q matplotlib numpy

echo "Generating graphs..."
python ssd_bench_analyze.py "$@"

echo "Done!"
