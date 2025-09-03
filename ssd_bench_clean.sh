#!/usr/bin/env bash
set -euo pipefail

# Remove generated JSON output files and analysis results while
# preserving committed summaries.

echo "Removing generated files..."
for dir in *_results; do
  [ -d "$dir" ] || continue
  echo "Cleaning $dir"
  rm -f "$dir"/*.json
  if [ -d "$dir/results" ]; then
    find "$dir/results" -type f ! -name summary.csv -delete
  fi
done

rm -rf results
echo "Cleanup complete."
