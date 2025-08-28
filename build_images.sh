#!/usr/bin/env bash
set -euo pipefail

# Create a virtual environment for running the analyzer
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

pip install matplotlib numpy

python analyze_fio_results.py
