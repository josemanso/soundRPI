# phaser real time
import numpy as np
import pyaudio
import time
import queue as queue
from scipy.signal import sawtooth
#import matplotlib.pyplot as plt

# dispositivo de entrada / salida
dev_index = 2 # device index found by p.get_device_info
# parecido a flanger, cambindo el lfo, con una un señal diente de sierra
RATE = 44100
f_lfo = 0.5 # menor de 1 Hz


# crear una onda diente de sierra
index = np.arange(0,1024,1)
lfo = 10* sawtooth(2 *np.pi * f_lfo *index / 50)
#plt.plot(lfo)
#plt.show()

q = np.ndarray([])
q = queue.Queue(2) #para guardar el anterior, in_data y el actual
y = np.zeros(1024)


pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # tiempo
    c = np.random.randint(100)
    if c == 30:
        s = time.time()
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    #array_data = np.append(q.get(), data)
    q.put(data)
    global y
    
    if q.full():
        # cogemos la última FIFO
        last_data = q.get()
        # hacemos el computo
        for i in range(1024):
            M = int(abs(lfo[i]))
            if i-M < 0:
                dato1 = last_data[1024+i-M]# datos del anterior
               
            else:
                dato1 = data[i-M]
            #y[n] = x[n] - x[n+del[lfo]]
            y[i] = data[i]+ dato1
    y = y/2
        
    sample = y.astype(np.int16).tostring()
    if c == 30:
        print('tiempo phaser: ', time.time() - s)
    return (sample, pyaudio.paContinue)

# open stream
stream = pa.open(
        format = pyaudio.paInt16,
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