import numpy as np
import matplotlib.pyplot as plt
import spec

data = np.load('fluct_1us.npy')
t = np.arange(len(data)) * 1.0e-6
n = 4096
w = np.hanning(n)
w = spec.normalize_area(w)
(yt, f, t_spec) = spec.spectrogram(data, w)
ts = t[1] - t[0] 
f /= ts
t_spec *= ts
# plt.figure(figsize=(10, 6))
# plt.plot(data)
# plt.title('data points')
# plt.xlabel('Time (microseconds)')
# plt.ylabel('Signal Amplitude')
# plt.grid(True)
# plt.show()

from scipy.signal import welch
# Parameters
fs = 1e6 # sampling frequency in Hz
window_size = 4096 # initial window size
# Compute power spectral density (PSD) using the Welch method
frequencies, psd = welch(data, fs=fs, nperseg=window_size)
# # Plot the PSD
# plt.figure(figsize=(10, 6))
# plt.semilogy(frequencies, psd)
# plt.title('Power Spectral Density with Window Size of 4096')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD')
# plt.grid(True)
# plt.show()


# # peak = np.argmax(psd)
# # peak_frequency = frequencies[peak]
# # print(peak_frequency)

