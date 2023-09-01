import numpy as np
import matplotlib.pyplot as plt

def spectrogram(y, w=np.array([]), nstep=0):  # y is a (100000, 1) matrix
    if w.size == 0:
        if nstep == 0:
            nstep = 1024
        w = np.ones(nstep) # area and height normalizations are the same for a rectangular window
    i = np.argwhere(w > (np.max(w) * 0.5)) # half max points
    t0 = (i[0][0] + i[-1][0]) / 2 # window center
    if nstep == 0:
        nstep = i[-1][0] - i[0][0] + 1
    i = np.arange(0, y.size - w.size + 1, nstep)
    i = i[:, np.newaxis] + np.arange(w.size)[np.newaxis, :]
    yt = y[i] * w[np.newaxis, :]  # y[i] change the dimension of y to 2
    yt = np.fft.ifft(yt, axis=1) # "forward" transform in the lecture note
    nh = w.size // 2 # only half the data needed for a real signal
    yt = yt[:, 0:(nh + 1)]
    f = np.arange(nh + 1) / w.size # normalized frequency
    t = np.arange(yt.shape[0]) * nstep + t0 # time at window center
    return (yt, f, t)

def normalize_area(w):
    return w * np.sqrt(w.size / np.sum(w**2))

def normalize_height(w):
    return w * (w.size / np.sum(w))

def flattop(n):
    w = 2.0 * np.pi * np.arange(n) / n
    w = (1.0 - 1.93 * np.cos(w) + 1.29 * np.cos(2.0 * w)
         - 0.388 * np.cos(3.0 * w) + 0.032 * np.cos(4 * w)) / 2.0
    return w

def find_index(x, xcut):
    xm = (x[0:-1] + x[1:]) * 0.5
    return np.searchsorted(xm, xcut)

def plot2(x, y, z, cmap_name='jet', interpolation='nearest', clabel=''):
    cmap = plt.get_cmap(cmap_name)
    dx = (x[1] - x[0]) * 0.5
    dy = (y[1] - y[0]) * 0.05
    x1 = x[0] - dx
    x2 = x[-1] + dx
    y1 = y[0] - dy
    y2 = y[-1] + dy
    plt.imshow(z, aspect='auto', interpolation=interpolation,
               origin='lower', extent=(x1, x2, y1, y2), cmap=cmap)
    plt.colorbar(label=clabel)
 
