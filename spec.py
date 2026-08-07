"""Windowed spectrogram utilities for time-series signal analysis."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def spectrogram(
    y: np.ndarray, w: np.ndarray | None = None, nstep: int = 0
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute a windowed spectrogram of a real 1-D signal.

    Parameters
    ----------
    y : ndarray
        Input signal, shape (N,).
    w : ndarray, optional
        Window applied to each segment. Defaults to a rectangular window of
        length ``nstep`` (or 1024 samples if ``nstep`` is also unset).
    nstep : int, optional
        Number of samples to advance between successive windows. Defaults to
        the half-max width of ``w``.

    Returns
    -------
    yt : ndarray
        Complex spectrogram, shape (n_windows, w.size // 2 + 1).
    f : ndarray
        Normalized frequency bins (cycles/sample).
    t : ndarray
        Sample index at the center of each window.
    """
    if w is None:
        w = np.ones(nstep if nstep else 1024)
    # Area and height normalizations are equal for a rectangular window.
    i = np.argwhere(w > (np.max(w) * 0.5))  # half-max points
    t0 = (i[0][0] + i[-1][0]) / 2  # window center
    if nstep == 0:
        nstep = i[-1][0] - i[0][0] + 1
    i = np.arange(0, y.size - w.size + 1, nstep)
    i = i[:, np.newaxis] + np.arange(w.size)[np.newaxis, :]
    yt = y[i] * w[np.newaxis, :]  # reshapes y[i] to 2-D, one row per window
    yt = np.fft.ifft(yt, axis=1)  # "forward" transform, per lecture convention
    nh = w.size // 2  # only half the bins are needed for a real signal
    yt = yt[:, 0:(nh + 1)]
    f = np.arange(nh + 1) / w.size  # normalized frequency
    t = np.arange(yt.shape[0]) * nstep + t0  # sample index at window center
    return yt, f, t


def normalize_area(w: np.ndarray) -> np.ndarray:
    """Scale a window so different window shapes yield equal noise power."""
    return w * np.sqrt(w.size / np.sum(w ** 2))


def normalize_height(w: np.ndarray) -> np.ndarray:
    """Scale a window so its values average to 1 (equal peak height)."""
    return w * (w.size / np.sum(w))


def flattop(n: int) -> np.ndarray:
    """Return an n-point flat-top window (low amplitude ripple, wide main lobe)."""
    w = 2.0 * np.pi * np.arange(n) / n
    return (
        1.0 - 1.93 * np.cos(w) + 1.29 * np.cos(2.0 * w)
        - 0.388 * np.cos(3.0 * w) + 0.032 * np.cos(4 * w)
    ) / 2.0


def find_index(x: np.ndarray, xcut: float) -> int:
    """Find the index of the bin in ``x`` whose midpoint is closest to ``xcut``."""
    xm = (x[0:-1] + x[1:]) * 0.5
    return int(np.searchsorted(xm, xcut))


def plot2(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    cmap_name: str = "jet",
    interpolation: str = "nearest",
    clabel: str = "",
) -> None:
    """Plot a 2-D array ``z`` as an image over axes ``x`` (columns) and ``y`` (rows)."""
    cmap = plt.get_cmap(cmap_name)
    dx = (x[1] - x[0]) * 0.5
    dy = (y[1] - y[0]) * 0.5
    x1, x2 = x[0] - dx, x[-1] + dx
    y1, y2 = y[0] - dy, y[-1] + dy
    plt.imshow(
        z, aspect="auto", interpolation=interpolation,
        origin="lower", extent=(x1, x2, y1, y2), cmap=cmap,
    )
    plt.colorbar(label=clabel)

