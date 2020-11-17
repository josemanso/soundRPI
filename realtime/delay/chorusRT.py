# chorus RT
import numpy as np
import pyaudio
import time
import queue as queue
#import matplotlib.pyplot as plt

CHUNK = 1024*2 # pyaudi por defecto nos toma 1024 frames
 # por interacción, haremos la computación con dos chunk
RATE = 44100
# chorus parameters
index = np.arange(CHUNK)
rate1 = 7
rate2 = 10

A = 10 # amplitud
lfo1 = A*np.sin(2*np.pi*index*rate1/CHUNK)
lfo2 = A*np.sin(2*np.pi*index*rate2/CHUNK)

#delay1 = 880 # 20 ms
#delay2 = 441 # 10 ms700
# ganancias 1
g = 0.20 


delay1 = int(0.040*RATE) # 40 ms
delay2 = int(0.010*RATE) # 

# tomaremos dos chunk
q = np.ndarray([])
q = queue.Queue(2) # dos chunks


#sample = np.zeros(1024)
pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = np.frombuffer(in_data, np.int16)# ndarray
    
    data_c = data.copy()
    q.put(data)
    if q.full():
        # cogemos la última FIFO
        last_data = q.get()
        # hacemos el computo
        for i in range(len(data)):
            M1 = delay1 + int(lfo1[i])
            #M1 = delay1 + np.random.randint(5)
            M2 = delay2 + int(lfo2[i])
            #M2 = delay3 + np.random.randint(5)
            if i-M1 < 0:
                dato1 = last_data[1024 +i-M1]
            else:
                dato1 = data[i-M1]
                
            if i-M2 < 0:
                dato2 = last_data[1024 +i-M2]
            else:
                dato2 = data[i-M2]
            data_c[i] = data[i] + dato1 + dato2
            
    data_c = data_c/ 2.5 # atenuamos
    data_c = data_c.astype(np.int16).tostring()
    #sample = np.array(data, dtype='int16')
    return (data_c, pyaudio.paContinue)
# open stream
stream = pa.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        input = True,
        output = True,
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