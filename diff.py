"""Compare beat-note frequency and amplitude of two mixers against the LO."""
from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from utils import load_measurement, plot_vs_control_voltage

LO_FREQUENCY_GHZ = 26.938


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lo-file", default="LO_240704.txt")
    parser.add_argument("--mixer1-file", default="mixer478_ch1_240704.txt")
    parser.add_argument("--mixer2-file", default="mixer479_ch1_240704.txt")
    parser.add_argument(
        "--lo-frequency", type=float, default=LO_FREQUENCY_GHZ,
        help="Local oscillator frequency in GHz",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    lo_data = load_measurement(args.lo_file)
    mixer1 = load_measurement(args.mixer1_file)
    mixer2 = load_measurement(args.mixer2_file)

    control_voltage = lo_data[:, 0]
    frequency = lo_data[:, 1]

    beat_frequency1 = abs(abs(args.lo_frequency - frequency * 2) - abs(mixer1[:, 1]))
    beat_frequency2 = abs(abs(args.lo_frequency - frequency * 2) - abs(mixer2[:, 1]))
    measured_frequency1 = abs(mixer1[:, 1])
    measured_frequency2 = abs(mixer2[:, 1])
    amplitude1 = mixer1[:, 2]
    amplitude2 = mixer2[:, 2]

    labels = ["478-1", "479-2"]
    colors = ["r", "g"]

    plt.figure(1)
    plt.subplot(211)
    plot_vs_control_voltage(
        control_voltage, [beat_frequency1, beat_frequency2], labels, colors,
        ylabel="Frequency (GHz)", title="Beat Frequency vs Control Voltage",
    )
    plt.subplot(212)
    plot_vs_control_voltage(
        control_voltage, [measured_frequency1, measured_frequency2], labels, colors,
        ylabel="Frequency (GHz)", title="Mixer Frequency vs Control Voltage",
    )

    plt.figure(2)
    plot_vs_control_voltage(
        control_voltage, [amplitude1, amplitude2], labels, colors,
        ylabel="Amplitude (dBm)", title="Amplitude vs Control Voltage",
    )

    plt.show()


if __name__ == "__main__":
    main()
