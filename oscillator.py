import numpy as np

data = np.loadtxt("oscillator.txt")
data1 = np.loadtxt("oscillator1.txt")
data2 = np.loadtxt("reference.txt")
control_voltage = data[:, 0]
frequency = data[:, 1]

import matplotlib.pyplot as plt
# measured data
plt.plot(control_voltage, frequency, 'r')
# reference data
plt.plot(data1[:, 0], data1[:, 1], 'g')
plt.plot(data2[:, 0], data2[:, 1], 'b')
plt.xlabel("Control Voltage (V)")
plt.ylabel("Frequency (Hz)")
plt.title("Frequency vs Control Voltage")
plt.legend(["240702", "240704","Reference"])
plt.show()