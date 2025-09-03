#!/usr/bin/env python3
"""Generate graphs from FIO result json files.

For each directory in the current working directory that ends with
``_results`` this script parses all ``*.json`` files and extracts
bandwidth, IOPS and CPU usage information.  Summary graphs are written to
a new ``results`` subdirectory inside each of those folders.
"""
from __future__ import annotations

import json
from pathlib import Path
import matplotlib.pyplot as plt
import csv
import numpy as np
import logging

# The repository may be executed from anywhere.  Find all sibling
# directories ending with ``_results`` relative to this script.
ROOT = Path(__file__).resolve().parent
logging.basicConfig(level=logging.INFO, format="%(message)s")


def process_results_directory(
    dir_path: Path,
) -> dict[str, tuple[float, float, float]]:
    """Parse all json files in *dir_path* and create graphs.

    A ``results`` subdirectory will be created to hold the generated
    graphs and a ``summary.csv`` file mapping the raw json file names to
    the values plotted.

    Returns a mapping from json stem names to
    ``(bandwidth_MiB_s, iops, avg_cpu_percent)`` values for aggregation
    across runs.
    """

    logging.info("Processing %s", dir_path)
    json_files = sorted(dir_path.glob("*.json"))
    if not json_files:
        logging.info("No json files found in %s", dir_path)
        return {}

    output_dir = dir_path / "results"
    output_dir.mkdir(exist_ok=True)

    names: list[str] = []
    bandwidths: list[float] = []
    iops_values: list[float] = []
    cpu_usages: list[float] = []

    data_map: dict[str, tuple[float, float, float]] = {}

    for jf in json_files:
        with open(jf) as fh:
            data = json.load(fh)
        job = data.get("jobs", [{}])[0]
        write_stats = job.get("write", {})
        read_stats = job.get("read", {})

        bw = write_stats.get("bw") or read_stats.get("bw") or 0
        iops = write_stats.get("iops") or read_stats.get("iops") or 0
        usr_cpu = job.get("usr_cpu", 0.0)
        sys_cpu = job.get("sys_cpu", 0.0)
        cpu_usage = usr_cpu + sys_cpu

        names.append(jf.stem)
        # FIO reports bandwidth in KiB/s.  Convert to MiB/s for readability.
        bw_mib = bw / 1024
        bandwidths.append(bw_mib)
        iops_values.append(iops)
        cpu_usages.append(cpu_usage)
        data_map[jf.stem] = (bw_mib, iops, cpu_usage)

    # Order results by bandwidth so graphs show steadily increasing bars.
    combined = sorted(
        zip(names, bandwidths, iops_values, cpu_usages), key=lambda x: x[1]
    )
    logging.info("Sorted entries: %s", [n for n, *_ in combined])
    names, bandwidths, iops_values, cpu_usages = (
        list(t) for t in zip(*combined)
    )

    # Save a CSV summary so values can be referenced against the original
    # json data.
    with open(output_dir / "summary.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file", "bandwidth_MiB_s", "iops", "avg_cpu_percent"])
        writer.writerows(zip(names, bandwidths, iops_values, cpu_usages))
    logging.info("Wrote %s", output_dir / "summary.csv")

    # Create a bandwidth bar chart.
    plt.figure(figsize=(10, 6))
    plt.bar(names, bandwidths)
    plt.ylabel("Bandwidth (MiB/s)")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Bandwidth for {dir_path.name}")
    plt.tight_layout()
    plt.savefig(output_dir / "bandwidth.png")
    logging.info("Saved %s", output_dir / "bandwidth.png")
    plt.close()

    # Create an IOPS bar chart.
    plt.figure(figsize=(10, 6))
    plt.bar(names, iops_values)
    plt.ylabel("IOPS")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"IOPS for {dir_path.name}")
    plt.tight_layout()
    plt.savefig(output_dir / "iops.png")
    logging.info("Saved %s", output_dir / "iops.png")
    plt.close()

    # Create a CPU usage bar chart.
    plt.figure(figsize=(10, 6))
    plt.bar(names, cpu_usages)
    plt.ylabel("CPU usage (%)")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"CPU usage for {dir_path.name}")
    plt.tight_layout()
    plt.savefig(output_dir / "cpu_usage.png")
    logging.info("Saved %s", output_dir / "cpu_usage.png")
    plt.close()

    return data_map


def aggregate_results(
    all_runs: dict[str, dict[str, tuple[float, float, float]]]
) -> None:
    """Generate combined graphs comparing all runs side by side."""

    if not all_runs:
        logging.info("No runs found")
        return

    output_dir = ROOT / "results"
    output_dir.mkdir(exist_ok=True)

    # Prepare data for grouped bar charts.
    runs = sorted(all_runs)
    files_set = {fname for mapping in all_runs.values() for fname in mapping}

    # Order file groups by their highest bandwidth to keep charts increasing.
    def file_sort_key(name: str) -> float:
        return max(all_runs[run].get(name, (0, 0, 0))[0] for run in runs)

    files = sorted(files_set, key=file_sort_key)

    # Write a sorted summary CSV referencing all raw data.
    rows = []
    for run in runs:
        for file, (bw, iops, cpu) in all_runs[run].items():
            rows.append((file, run, bw, iops, cpu))
    rows.sort(key=lambda r: (file_sort_key(r[0]), runs.index(r[1])))
    with open(output_dir / "summary.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file", "run", "bandwidth_MiB_s", "iops", "avg_cpu_percent"])
        writer.writerows(rows)
    logging.info("Wrote %s", output_dir / "summary.csv")
    bandwidth_matrix = [[all_runs[run].get(f, (0, 0, 0))[0] for f in files] for run in runs]
    iops_matrix = [[all_runs[run].get(f, (0, 0, 0))[1] for f in files] for run in runs]
    cpu_matrix = [[all_runs[run].get(f, (0, 0, 0))[2] for f in files] for run in runs]

    x = np.arange(len(files))
    width = 0.8 / len(runs)

    plt.figure(figsize=(10, 6))
    for idx, run in enumerate(runs):
        plt.bar(x + idx * width, bandwidth_matrix[idx], width=width, label=run)
    plt.ylabel("Bandwidth (MiB/s)")
    plt.xticks(x + width * (len(runs) - 1) / 2, files, rotation=45, ha="right")
    plt.title("Bandwidth comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "bandwidth.png")
    logging.info("Saved %s", output_dir / "bandwidth.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    for idx, run in enumerate(runs):
        plt.bar(x + idx * width, iops_matrix[idx], width=width, label=run)
    plt.ylabel("IOPS")
    plt.xticks(x + width * (len(runs) - 1) / 2, files, rotation=45, ha="right")
    plt.title("IOPS comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "iops.png")
    logging.info("Saved %s", output_dir / "iops.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    for idx, run in enumerate(runs):
        plt.bar(x + idx * width, cpu_matrix[idx], width=width, label=run)
    plt.ylabel("CPU usage (%)")
    plt.xticks(x + width * (len(runs) - 1) / 2, files, rotation=45, ha="right")
    plt.title("CPU usage comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "cpu_usage.png")
    logging.info("Saved %s", output_dir / "cpu_usage.png")
    plt.close()


def main() -> None:
    all_runs: dict[str, dict[str, tuple[float, float, float]]] = {}
    for directory in ROOT.iterdir():
        if directory.is_dir() and directory.name.endswith("_results"):
            all_runs[directory.name] = process_results_directory(directory)

    aggregate_results(all_runs)


if __name__ == "__main__":
    main()
