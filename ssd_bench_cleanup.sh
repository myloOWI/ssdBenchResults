#!/usr/bin/env bash
set -euo pipefail

# Remove generated JSON output files and analysis results.

for dir in *_results; do
  [ -d "$dir" ] || continue
  rm -f "$dir"/*.json
  rm -rf "$dir"/results
done

rm -rf results
