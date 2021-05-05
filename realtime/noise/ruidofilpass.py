# reducción de ruidocon filtro paso banda
import os
import numpy as np
import pyaudio
import time
from scipy.signal import butter, lfilter

# con la gráfica del fft del audio /sonido/fftdata.py
# cojemos la frecuencias que suponemos
# mayores  entonces ruido, menores... entonces ruido
RATE = 44100
fs = RATE
order = 3#7
beginFreq = 200/(fs/2)#700/(fs/2)
endFreq = 11000/(fs/2)#12000/(fs/2)
#b, a = butter(order,4000/(fs/2), btype ='low')
b,a = butter(order, [beginFreq,endFreq], btype='band')




def callback(in_data, frame_count, time_info, status):
    
    data = np.frombuffer(in_data, np.int16)
    filtered_d = lfilter(b, a, data)
    
    filtered_d = filtered_d.astype(np.int16).tobytes()
    return (filtered_d, pyaudio.paContinue)

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