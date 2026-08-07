"""Compare measured VCO tuning curves against reference data."""
from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from utils import load_measurement, plot_vs_control_voltage


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--measured-file", default="oscillator.txt")
    parser.add_argument("--measured-file2", default="oscillator1.txt")
    parser.add_argument("--reference-file", default="reference.txt")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    measured = load_measurement(args.measured_file)
    measured2 = load_measurement(args.measured_file2)
    reference = load_measurement(args.reference_file)

    plot_vs_control_voltage(
        measured[:, 0],
        [measured[:, 1], measured2[:, 1], reference[:, 1]],
        ["240702", "240704", "Reference"],
        ["r", "g", "b"],
        ylabel="Frequency (Hz)",
        title="Frequency vs Control Voltage",
    )
    plt.show()


if __name__ == "__main__":
    main()
