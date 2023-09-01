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

n2 = 4096
w2 = spec.flattop(n2)
w2 = spec.normalize_height(w2)
(yt2, f2, t_spec2) = spec.spectrogram(data, w2)
f2 /= ts
t_spec2 *= ts
fcut = 239990.234375 # [Hz]
i = spec.find_index(f2, fcut)
a = np.abs(yt2[:, i]) * 2.0
# plt.figure(3)
# plt.plot(t_spec2, a)
# plt.ylim((0, plt.ylim()[1]*1.5))
# plt.xlabel('time [s]')
# plt.ylabel('amplitude [V]')
# plt.title('frequency = {:.3g} kHz'.format(fcut*1e-3))
# plt.show()

threshold = 0.6 * np.max(np.abs(a))
# Find where the signal exceeds the threshold
over_threshold = np.where(np.abs(a) > threshold)[0]
# Compute the duration based on the start and end of the signal
duration = (over_threshold[-1] - over_threshold[0]) / fs

print(duration)q