import soundfile as sf
import numpy as np
from scipy import signal
from math import ceil, log

def chirp2ir(input_, ref_sig,fs, window=True, f_low=100, f_high=8000):
    nfft = 2**(ceil(log(len(input_), 2)))
    
    if window:
        ## removing bias/ dc-offset by bandpass filter##
        sos = signal.butter(3, [f_low, f_high], 'bp', output='sos', fs=fs)
        filt_sig = signal.sosfilt(sos, input_)
        filt_sig /= max(abs(filt_sig))
    else:
        ## Remark: By not filtering we are not compensating for the DC-offset
        filt_sig = input_
    
    ### TO DO ### extend to multichannels....
    # dimension to take fft along
    ir = np.fft.irfft(np.fft.rfft(ref_sig, nfft) / np.fft.rfft(filt_sig, nfft))


if __name__=='__main__':
    chirp2ir("measured_sig.wav", "chirp.wav", fs, window=True, f_low=100, f_high=8000)