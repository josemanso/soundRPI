# fitrado del ruido de fondo(hiss, hum)
import os
import numpy as np
import pyaudio
import time
from scipy.signal import butter, lfilter

RATE=44100 # Hz
fs = 44100
order = 3#7
beginFreq = 200/(fs/2)#700/(fs/2)
endFreq = 11000/(fs/2)#12000/(fs/2)
b,a = butter(order, [beginFreq,endFreq], btype='band')
print('b ', b, ' a ', a)

def noise_reduction_filtr(signal_in):
    return lfilter(b, a, signal_in)

def callback(in_data, frame_count, time_info, status):
    
    data = np.frombuffer(in_data, np.int16)
    y = noise_reduction_filtr(data)
    #y = np.real(y)
    
    #print('y', y.dtype)
    new_y = y.astype(np.int16)
    #print('n_y', new_y)
    #y = y.astype(np.int16).tobytes()
    new_y = new_y.tobytes()
    return (new_y, pyaudio.paContinue)
    #return (data, pyaudio.paContinue)

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