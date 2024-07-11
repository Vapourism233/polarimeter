import numpy as np
import matplotlib.pyplot as plt

def splitter(data):
    x = data[:,0]
    ch1 = data[:,1]
    ch2 = data[:,2]
    ch3 = data[:,3]
    ch4 = data[:,4]
    ref = data[:,5]

    return x, ch1, ch2, ch3, ch4, ref
    # plt.plot(x, ch1, label='ch1', color='red')
    # plt.plot(x, ch2, label='ch2', color='blue')
    # plt.plot(x, ch3, label='ch3', color='green')
    # plt.plot(x, ch4, label='ch4', color='black')
    # plt.legend()
    # plt.show()

def lo(LO, mixer1, mixer2, mixer3, mixer4):
    freq = LO[:, 1]
    frequency1 = abs(abs(mixer1[:, 2] - freq*2) - abs(mixer1[:, 1]))
    Freq1 = abs(mixer1[:, 1])
    error1 = np.mean(frequency1 / Freq1)
    frequency2 = abs(abs(mixer2[:, 2] - freq*2) - abs(mixer2[:, 1]))
    Freq2 = abs(mixer2[:, 1])
    error2 = np.mean(frequency2 / Freq2)
    frequency3 = abs(abs(mixer3[:, 2] - freq*2) - abs(mixer3[:, 1]))
    Freq3 = abs(mixer3[:, 1])
    error3 = np.mean(frequency3 / Freq3)
    frequency4 = abs(abs(mixer4[:, 2] - freq*2) - abs(mixer4[:, 1]))
    Freq4 = abs(mixer4[:, 1])
    error4 = np.mean(frequency4 / Freq4)
    amplitude1 = mixer1[:, 3]
    amplitude2 = mixer2[:, 3]
    amplitude3 = mixer3[:, 3]
    amplitude4 = mixer4[:, 3]
    return frequency1, frequency2, frequency3, frequency4, amplitude1, amplitude2, amplitude3, amplitude4, error1, error2, error3, error4



if __name__ == '__main__':

    # sp = np.loadtxt('splitter_240708.txt')
    sp = np.loadtxt('splitter_240710.txt')
    LO = np.loadtxt('LO_240704.txt')
    mixer478_ch1 = np.loadtxt('mixer478_ch1_240708.txt')
    mixer479_ch1 = np.loadtxt('mixer479_ch1_240708.txt')
    mixer478_ch2 = np.loadtxt('mixer478_ch2_240708.txt')
    mixer479_ch2 = np.loadtxt('mixer479_ch2_240708.txt')
    control_voltage = LO[:, 0]
    x, ch1, ch2, ch3, ch4, ref = splitter(sp)
    
    frequency1, frequency2, frequency3, frequency4, amplitude1, amplitude2, amplitude3, amplitude4, error1, error2, error3, error4 = lo(LO, mixer478_ch1, mixer479_ch1, mixer478_ch2, mixer479_ch2)

    # # plot splitter
    # plt.figure(1)
    # plt.plot(x, ch1, 'r')
    # plt.plot(x, ch2, 'g')
    # plt.plot(x, ch3, 'b')
    # plt.plot(x, ch4, 'k')
    # plt.xlabel("Control Voltage (V)")
    # plt.ylabel("Splitter Channel Amplitude [dBm]")
    # plt.title("Splitter Channel Amplitude vs Control Voltage")
    # plt.legend(["ch1", "ch2", "ch3", "ch4"])
    # plt.tight_layout()

    # plt.figure(2)
    # plt.plot(control_voltage, amplitude1, 'r')
    # plt.plot(control_voltage, amplitude2, 'g')
    # plt.plot(control_voltage, amplitude3, 'b')
    # plt.plot(control_voltage, amplitude4, 'k')
    # plt.xlabel("Control Voltage (V)")
    # plt.ylabel("Amplitude [dBm]")
    # plt.title("Amplitude vs Control Voltage")
    # plt.legend(["478-ch1", "479-ch1", "478-ch2", "479-ch2"])
    # plt.tight_layout()

    # # the error of frequency of the beating signal from LO and mixer
    # plt.figure(3)
    # plt.plot(control_voltage, frequency1, 'r')
    # plt.plot(control_voltage, frequency2, 'g')
    # plt.plot(control_voltage, frequency3, 'b')
    # plt.plot(control_voltage, frequency4, 'k')
    # plt.xlabel("Control Voltage (V)")
    # plt.ylabel("Frequency (GHz)")
    # plt.title("Beating signal frequency vs Control Voltage")
    # plt.legend(["478-ch1", "479-ch1", "478-ch2", "479-ch2"])
    # print("The error of calculation and measurement is:", error1, error2, error3, error4)
    # plt.tight_layout()

    # inversion loss
    plt.figure(1)
    plt.subplot(211)
    plt.plot(x, ref - ch1, 'r')
    plt.plot(x, ref - ch2, 'g')
    plt.plot(x, ref - ch3, 'b')
    plt.plot(x, ref - ch4, 'k')

    plt.xlabel("Control Voltage (V)")
    plt.ylabel("Inversion Loss [dB]")
    plt.title("Inversion Loss vs Control Voltage")
    plt.legend(["ch1", "ch2", "ch3", "ch4"])
    plt.tight_layout()

    # the ratio of the amplitude from every channel
    plt.subplot(212)
    plt.plot(x, ch1 / ref, 'r')
    plt.plot(x, ch2 / ref, 'g')
    plt.plot(x, ch3 / ref, 'b')
    plt.plot(x, ch4 / ref, 'k')
    plt.xlabel("Control Voltage (V)")
    plt.ylabel("Amplitude Ratio")
    plt.title("Amplitude Ratio vs Control Voltage")
    plt.legend(["ch1", "ch2", "ch3", "ch4"])
    plt.tight_layout()

    plt.show()


