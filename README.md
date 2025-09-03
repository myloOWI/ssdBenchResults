# SSD Benchmark Scripts

This repository provides simple helpers for running FIO-based SSD benchmarks and visualizing the results.

## Usage

1. **Run tests**
   ```bash
   cd <target_results_directory>
   ../ssd_bench_run.sh [path_to_test_file]
   ```
   JSON output files are written into the current directory.

2. **Generate graphs**
   ```bash
   cd ..
   ./ssd_bench_plot.sh
   ```
   Graphs and `summary.csv` files are written under each `*_results/results` folder as well as a top-level `results` directory.

3. **Cleanup**
   ```bash
   ./ssd_bench_clean.sh
   ```
   Removes generated JSON and analysis artifacts.

## Requirements
- bash
- Python 3 with `venv`
- `fio` for running the tests
