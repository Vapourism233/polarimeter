"""Analyze splitter channel balance and LO/mixer beat-frequency consistency."""
from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from utils import load_measurement, plot_vs_control_voltage


def splitter(data: np.ndarray):
    """Split a splitter measurement file into its column components."""
    x = data[:, 0]
    ch1, ch2, ch3, ch4, ref = (data[:, i] for i in range(1, 6))
    return x, ch1, ch2, ch3, ch4, ref


def lo(lo_data: np.ndarray, mixer1: np.ndarray, mixer2: np.ndarray, mixer3: np.ndarray, mixer4: np.ndarray):
    """Compute beat-note frequency/amplitude for four mixer channels against the LO.

    Returns per-channel beat frequency, amplitude, and the mean relative error
    between the calculated and measured beat frequency.
    """
    freq = lo_data[:, 1]
    frequencies, amplitudes, errors = [], [], []
    for mixer in (mixer1, mixer2, mixer3, mixer4):
        beat = abs(abs(mixer[:, 2] - freq * 2) - abs(mixer[:, 1]))
        measured = abs(mixer[:, 1])
        frequencies.append(beat)
        amplitudes.append(mixer[:, 3])
        errors.append(np.mean(beat / measured))
    return frequencies, amplitudes, errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--splitter-file", default="splitter_240710.txt")
    parser.add_argument("--lo-file", default="LO_240704.txt")
    parser.add_argument("--mixer478-ch1", default="mixer478_ch1_240708.txt")
    parser.add_argument("--mixer479-ch1", default="mixer479_ch1_240708.txt")
    parser.add_argument("--mixer478-ch2", default="mixer478_ch2_240708.txt")
    parser.add_argument("--mixer479-ch2", default="mixer479_ch2_240708.txt")
    parser.add_argument(
        "--diagnostics", action="store_true",
        help="Also plot per-channel splitter amplitude, mixer amplitude, and beat-frequency error",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    sp = load_measurement(args.splitter_file)
    lo_data = load_measurement(args.lo_file)
    mixer478_ch1 = load_measurement(args.mixer478_ch1)
    mixer479_ch1 = load_measurement(args.mixer479_ch1)
    mixer478_ch2 = load_measurement(args.mixer478_ch2)
    mixer479_ch2 = load_measurement(args.mixer479_ch2)

    control_voltage = lo_data[:, 0]
    x, ch1, ch2, ch3, ch4, ref = splitter(sp)
    channel_labels = ["478-ch1", "479-ch1", "478-ch2", "479-ch2"]
    colors = ["r", "g", "b", "k"]

    frequencies, amplitudes, errors = lo(
        lo_data, mixer478_ch1, mixer479_ch1, mixer478_ch2, mixer479_ch2
    )

    if args.diagnostics:
        plt.figure("splitter-channels")
        plot_vs_control_voltage(
            x, [ch1, ch2, ch3, ch4], ["ch1", "ch2", "ch3", "ch4"], colors,
            ylabel="Splitter Channel Amplitude (dBm)",
            title="Splitter Channel Amplitude vs Control Voltage",
        )

        plt.figure("mixer-amplitude")
        plot_vs_control_voltage(
            control_voltage, amplitudes, channel_labels, colors,
            ylabel="Amplitude (dBm)", title="Amplitude vs Control Voltage",
        )

        plt.figure("beat-frequency")
        plot_vs_control_voltage(
            control_voltage, frequencies, channel_labels, colors,
            ylabel="Frequency (GHz)", title="Beating Signal Frequency vs Control Voltage",
        )
        print("Mean relative error between calculated and measured beat frequency:")
        for label, error in zip(channel_labels, errors):
            print(f"  {label}: {error:.3g}")

    plt.figure("inversion-loss")
    plt.subplot(211)
    plot_vs_control_voltage(
        x, [ref - ch1, ref - ch2, ref - ch3, ref - ch4], ["ch1", "ch2", "ch3", "ch4"], colors,
        ylabel="Inversion Loss (dB)", title="Inversion Loss vs Control Voltage",
    )
    plt.subplot(212)
    plot_vs_control_voltage(
        x, [ch1 / ref, ch2 / ref, ch3 / ref, ch4 / ref], ["ch1", "ch2", "ch3", "ch4"], colors,
        ylabel="Amplitude Ratio", title="Amplitude Ratio vs Control Voltage",
    )

    plt.show()


if __name__ == "__main__":
    main()

