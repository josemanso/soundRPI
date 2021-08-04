# Susbtracción espectral del ruido
import os
import numpy as np
import pyaudio
import time
from scipy.fftpack import fft, ifft
from scipy.signal import hann


RATE = 44100
# 50000 hacemos un filtro a PSD, que es(a+bi)*(a-bi), 
# y descartamos lo valores mayores de 50000, esto se hace de forma visual
# haciendo la gráfica de PSD y viendo los valores que son ruido
def noise_reduction_fft(data_in):
    n = len(data_in)
    fft_data= fft(data_in,n)
    PSD = PSD = fft_data * np.conj(fft_data) / n
    indices = PSD > 50000  # finf all frequenciies with large power
    filtered = fft_data*indices
    filt = ifft(filtered)
    return filt


def callback(in_data, frame_count, time_info, status):
    # tiempo
    c = np.random.randint(100)
    if c == 30:
        s = time.time()
    data = np.frombuffer(in_data, np.int16)
    y = noise_reduction_fft(data)
    
    y = np.real(y)
    
    new_y = y.astype(np.int16)
    
    new_y = new_y.tobytes()
    if c == 30:
        print('tiempo sustracción espectral del ruido: ', time.time() - s)

    return (new_y, pyaudio.paContinue)

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