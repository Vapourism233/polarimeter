import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("LO_240704.txt")
mixer = np.loadtxt("mixer478_ch1_240704.txt")
mixer1 = np.loadtxt("mixer479_ch1_240704.txt")
LO = 26.938 # GHz
control_voltage = data[:, 0]
frequency = data[:, 1]
frequency1 = abs(abs(LO - frequency*2) - abs(mixer[:, 1]))
Freq1 = abs(mixer[:, 1])
frequency2 = abs(abs(LO - frequency*2) - abs(mixer1[:, 1]))
Freq2 = abs(mixer1[:, 1])
amplitude1 = mixer[:, 2]
amplitude2 = mixer1[:, 2]
# 3 plots, two for frequency and one for amplitude
plt.figure(1)
plt.subplot(211)
plt.plot(control_voltage, frequency1, 'r')
plt.plot(control_voltage, frequency2, 'g')
plt.xlabel("Control Voltage (V)")
plt.ylabel("Frequency (GHz)")
plt.title("Frequency vs Control Voltage")
plt.legend(["478-1", "479-2"])

plt.subplot(212)
plt.plot(control_voltage, Freq1, 'r')
plt.plot(control_voltage, Freq2, 'g')
plt.xlabel("Control Voltage (V)")
plt.ylabel("Frequency (GHz)")
plt.title("Frequency vs Control Voltage")
plt.legend(["478-1", "479-2"])
plt.tight_layout()

plt.figure(2)
plt.plot(control_voltage, amplitude1, 'r')
plt.plot(control_voltage, amplitude2, 'g')
plt.xlabel("Control Voltage (V)")
plt.ylabel("Amplitude (dBm)")
plt.title("Amplitude vs Control Voltage")
plt.legend(["478-1", "479-2"])
plt.tight_layout()

plt.show()