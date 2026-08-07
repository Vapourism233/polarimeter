"""Shared I/O and plotting helpers used by the polarimeter analysis scripts."""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np


def load_measurement(path: str | Path) -> np.ndarray:
    """Load a whitespace-delimited measurement file into a 2-D array."""
    return np.loadtxt(path)


def plot_vs_control_voltage(
    x: np.ndarray,
    ys: Sequence[np.ndarray],
    labels: Sequence[str],
    colors: Sequence[str],
    ylabel: str,
    title: str,
    xlabel: str = "Control Voltage (V)",
) -> None:
    """Plot one or more series on shared axes with a consistent style."""
    for y, label, color in zip(ys, labels, colors):
        plt.plot(x, y, color, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
