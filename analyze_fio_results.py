#!/usr/bin/env python3
"""Generate graphs from FIO result json files.

For each directory in the current working directory that ends with
``_results`` this script parses all ``*.json`` files and extracts
bandwidth and IOPS information.  Summary graphs are written to a new
``results`` subdirectory inside each of those folders.
"""
from __future__ import annotations

import json
from pathlib import Path
import matplotlib.pyplot as plt
import csv

# The repository may be executed from anywhere.  Find all sibling
# directories ending with ``_results`` relative to this script.
ROOT = Path(__file__).resolve().parent


def process_results_directory(dir_path: Path) -> None:
    """Parse all json files in *dir_path* and create graphs.

    A ``results`` subdirectory will be created to hold the generated
    graphs and a ``summary.csv`` file mapping the raw json file names to
    the values plotted.
    """

    json_files = sorted(dir_path.glob("*.json"))
    if not json_files:
        return

    output_dir = dir_path / "results"
    output_dir.mkdir(exist_ok=True)

    names: list[str] = []
    bandwidths: list[float] = []
    iops_values: list[float] = []

    for jf in json_files:
        with open(jf) as fh:
            data = json.load(fh)
        job = data.get("jobs", [{}])[0]
        write_stats = job.get("write", {})
        read_stats = job.get("read", {})

        bw = write_stats.get("bw") or read_stats.get("bw") or 0
        iops = write_stats.get("iops") or read_stats.get("iops") or 0

        names.append(jf.stem)
        # FIO reports bandwidth in KiB/s.  Convert to MiB/s for readability.
        bandwidths.append(bw / 1024)
        iops_values.append(iops)

    # Save a CSV summary so values can be referenced against the original
    # json data.
    with open(output_dir / "summary.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file", "bandwidth_MiB_s", "iops"])
        writer.writerows(zip(names, bandwidths, iops_values))

    # Create a bandwidth bar chart.
    plt.figure(figsize=(10, 6))
    plt.bar(names, bandwidths)
    plt.ylabel("Bandwidth (MiB/s)")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Bandwidth for {dir_path.name}")
    plt.tight_layout()
    plt.savefig(output_dir / "bandwidth.png")
    plt.close()

    # Create an IOPS bar chart.
    plt.figure(figsize=(10, 6))
    plt.bar(names, iops_values)
    plt.ylabel("IOPS")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"IOPS for {dir_path.name}")
    plt.tight_layout()
    plt.savefig(output_dir / "iops.png")
    plt.close()


def main() -> None:
    for directory in ROOT.iterdir():
        if directory.is_dir() and directory.name.endswith("_results"):
            process_results_directory(directory)


if __name__ == "__main__":
    main()
