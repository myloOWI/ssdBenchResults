#!/usr/bin/env bash
set -euo pipefail

# Run FIO write tests for various job counts and file sizes.
# Output JSON files into the current directory.

device=${1:-/home/nvidia/nvme/test_file}

declare -a sizes=(2G 5G)
declare -a jobs=(1 2 3 4)

echo "Running SSD benchmark tests on $device"

for size in "${sizes[@]}"; do
  for job in "${jobs[@]}"; do
    echo ">>> Starting ${job} job(s) (${size})..."
    name="smallfile_${job}_jobs"
    if [ "$size" = "5G" ]; then
      name+="_5g"
    fi
    fio --name="$name" \
        --filename="$device" \
        --ioengine=libaio \
        --rw=write \
        --bsrange=128k-10m \
        --size="$size" \
        --direct=1 \
        --numjobs="$job" \
        --iodepth=32 \
        --time_based --runtime=60 \
        --group_reporting \
        --output="${name}.json" \
        --output-format=json
    echo "<<< Finished ${job} job(s) (${size})"
  done
done

echo "=== All tests completed ==="
