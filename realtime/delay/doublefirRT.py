#  Doubling, double track, en tiempo real
import numpy as np
import pyaudio
import time
from scipy.signal import lfilter
import queue as queue

# dispositivo de entrada / salida
dev_index = 2 # device index found by p.get_device_info
# parámetros para el efecto doubling
delay = 280 #  5 ms 220 tramas
b = np.zeros(delay)
b[0]= 1 # señal1
b[-1]= 0.7 # retraso
#b /=sum(b)
#print('b ', b)


RATE =44100
q = np.ndarray([])
q = queue.Queue(1) #para guardar el anterior, in_data
aux = np.zeros(1024)
q.put(aux)

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    #b = False
    #tiempo1 = np.random.randint(100)
    c = np.random.randint(100)
    #b = False
    if c == 30:
        #b = True
        s = time.time()
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    array_data = np.append(q.get(), data)
    #print('array ', len(array_data))
    q.put(data)

    # hacemos el computo
    
    data_filt = lfilter(b,1,array_data) #/2
    y = data_filt[1024:]
    
    sample = y.astype(np.int16).tostring()
    if c ==30:
        print('tiempo double: ', time.time()-s)
        
    return (sample, pyaudio.paContinue)
# open stream
stream = pa.open(
        format = pyaudio.paInt16,#pa.get_format_from_width(2), # un byte
        channels = 1,
        rate = RATE,
        #input = True,
        #output = True,
        input_device_index = dev_index,input = True,
        output_device_index = dev_index,output = True,
        stream_callback = callback)
stream.start_stream()

while stream.is_active():
    print("Stream is active")
    time.sleep(10)
    stream.stop_stream()
    print("Stream is stopped")

stream.stop_stream()
stream.close()

pa.terminate()
