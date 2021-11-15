import numpy as np
import matplotlib.pyplot as plt

class FIRfilter:

    def __init__(self, _coefficients):
        self._coefficients = _coefficients
        self._ntaps = len(_coefficients)
        self._buffer = np.zeros(self._ntaps)

    #PART1
    ######################################
    #a) highpass filter
    @staticmethod
    def highpassDesign(sampling_rate, cutoff_frequencies, resolution=1):
        ntaps = int(sampling_rate/resolution)
        if ntaps%2 != 0: ntaps -=1
        f_c = int(cutoff_frequencies/sampling_rate * ntaps)
        taps_Arr = np.ones(ntaps)

        taps_Arr[0:f_c] = 0
        #taps_Arr[ntaps-f_c] = 0

        _h = FIRfilter.editing_h( taps_Arr )
        return _h

    #b) bandstop filter
    @staticmethod
    def bandstopDesign(sampling_rate, lowband, highband, resolution=1):
        ntaps = int(sampling_rate/resolution)
        if ntaps%2 != 0: ntaps -=1
        f_Low = int(lowband/sampling_rate * ntaps)
        f_High = int(highband/sampling_rate * ntaps)
        taps_Arr = np.ones(ntaps)

        taps_Arr[f_Low:f_High+1] = 0
        taps_Arr[ntaps-f_High:ntaps-f_Low+1] = 0

        _h = FIRfilter.editing_h( taps_Arr )
        return _h

    @staticmethod
    def editing_h(raw_h):
        tmp_h = np.fft.ifft(raw_h)
        tmp_h = np.real(tmp_h)
        h = np.ones(int(len(tmp_h)))
        h[0:int(len(h)/2)] = tmp_h[int(len(tmp_h)/2):len(tmp_h)]
        h[int(len(h)/2):len(h)] = tmp_h[0:int(len(tmp_h)/2)]
        h = h * np.hamming(len(h))
        return h

    #PART2
    ######################################
    def doFilter(self, v):
        output = 0
        for i in range(self._ntaps-1, 0, -1):
            self._buffer[i] = self._buffer[i-1]
        self._buffer[0] = v
        for i in range(0, self._ntaps):
            output += self._buffer[i] * self._coefficients[i]
        return output

    def doFilterAdaptive(self,signal,noise,learningRate):
        return scalar
if __name__ == '__main__':
    N = 5000
    s_rate = 250
    org_ECG = np.loadtxt('C:\\Users\\gcz_9\\Documents\\GitHub\\DSP_firFilter\\ECGs\\ECG_msc_matric_8.dat')

    coefficient_HP = FIRfilter.highpassDesign(s_rate, 50)
    coefficient_BS = FIRfilter.bandstopDesign(s_rate, 45, 55)

    ECG_filted_by_HP = []
    ECG_filted_by_BS = []

    HP_output = FIRfilter(coefficient_HP)
    BS_output = FIRfilter(coefficient_BS)

    for _i in range(0,N):
        ECG_filted_by_HP.append( HP_output.doFilter(org_ECG[_i]) )
    for _i in range(0,N):
        ECG_filted_by_BS.append( BS_output.doFilter(ECG_filted_by_HP[_i]) )
    plt.subplot(211)
    plt.title("ORG")
    plt.plot(org_ECG)
    plt.subplot(212)
    plt.title("filted")
    plt.plot(ECG_filted_by_BS)
    plt.show()
