"""Analyze fluctuation time-series data via windowed spectrograms.

Loads a time series sampled at a fixed rate and characterizes it two ways:
1. A Hann-windowed spectrogram, used to estimate a broadband power spectral
   density (PSD) via Welch's method.
2. A flat-top windowed spectrogram, used to track the amplitude of a single
   frequency bin over time and estimate how long the signal stays above a
   threshold.
"""
from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch

import spec


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="fluct_1us.npy", help="Path to the .npy time-series file")
    parser.add_argument("--sample-rate", type=float, default=1.0e6, help="Sampling frequency in Hz")
    parser.add_argument("--window-size", type=int, default=4096)
    parser.add_argument(
        "--target-frequency", type=float, default=239990.234375,
        help="Frequency bin (Hz) to track amplitude over time",
    )
    parser.add_argument(
        "--threshold-fraction", type=float, default=0.6,
        help="Fraction of peak amplitude used as the detection threshold",
    )
    parser.add_argument("--plot", action="store_true", help="Show diagnostic plots")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    fs = args.sample_rate
    dt = 1.0 / fs

    data = np.load(args.input)
    t = np.arange(len(data)) * dt

    # Broadband power spectral density via Welch's method.
    frequencies, psd = welch(data, fs=fs, nperseg=args.window_size)

    # Track a single frequency bin's amplitude over time with a flat-top window.
    flattop_window = spec.normalize_height(spec.flattop(args.window_size))
    yt, f, t_spec = spec.spectrogram(data, flattop_window)
    f /= dt
    t_spec *= dt

    target_index = spec.find_index(f, args.target_frequency)
    amplitude = np.abs(yt[:, target_index]) * 2.0

    threshold = args.threshold_fraction * np.max(amplitude)
    over_threshold = np.where(amplitude > threshold)[0]
    if over_threshold.size:
        duration = (over_threshold[-1] - over_threshold[0]) / fs
        print(f"Signal duration above threshold: {duration:.6g} s")
    else:
        print("Signal never exceeds the threshold.")

    if args.plot:
        plt.figure(figsize=(10, 6))
        plt.plot(t, data)
        plt.title("Time-Domain Signal")
        plt.xlabel("Time (s)")
        plt.ylabel("Signal Amplitude")
        plt.grid(True)

        plt.figure(figsize=(10, 6))
        plt.semilogy(frequencies, psd)
        plt.title(f"Power Spectral Density (window size = {args.window_size})")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("PSD")
        plt.grid(True)

        plt.figure(figsize=(10, 6))
        plt.plot(t_spec, amplitude)
        plt.ylim(0, plt.ylim()[1] * 1.5)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude (V)")
        plt.title(f"Frequency = {args.target_frequency * 1e-3:.3g} kHz")

        plt.show()


if __name__ == "__main__":
    main()

