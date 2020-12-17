# Susbtracción espectral del ruido
import sys
import os
import numpy as np
import pyaudio
import time
from scipy.io import wavfile
from scipy.fftpack import ifft, irfft
from scipy.signal import hann

noise = 121


def callback(in_data, frame_count, time_info, status):
    
    data = np.frombuffer(in_data, np.int16)
   
    global signal_in#, signal_out
    #signal_in = np.append(signal_in, data)
    #if len(signal_in) == 3072: #3x 1024 data
    y = noiseless(y_noise, data)
    #print('y  ', y.dtype)
    print('y  ', y)
    
    
        # hacemos el computo
        #signal_out = noiseless(signal_in)
        # quitamos el primer chunk
        #signal_in = signal_in[1024:]
    #y = y.astype(np.int16).tostring()
    
    #y = y.astype(np.int16).tobytes()
    return (y, pyaudio.paContinue)
    #return (data, pyaudio.paContinu
p = pyaudio.PyAudio()
## open stream using callback
stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        input = True,
        output = True,
        stream_callback = callback)

stream.start_stream()
try:
    while stream.is_active():
        print("Stream is active")
        time.sleep(12)
        stream.stop_stream()
        print("Stream is stopped")
except os.error as ex:
    print(ex)
    

stream.stop_stream()
stream.close()

p.terminate()
        