#vibratoRT
import numpy as np
import pyaudio
import time

RATE = 44100
# dispositivo de entrada / salida
dev_index = 2 # device index found by p.get_device_info
#  tipical delay, 5-10 ms, LFO 4-14 Hz

#la frecuencia de muestreo en tiempo real es un CHUNK

delay = 0.0010
fo = 10 #6 # Hz frec lfo
# real time
CHUNK = 1024 # valor por defecto pyaudio
index = np.arange(CHUNK)
lfo = np.sin(2*np.pi*index*fo/128)
#import matplotlib.pyplot as plt
#plt.plot(lfo)
#plt.show()

pa= pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    c = np.random.randint(100)
    if c == 30:
        s = time.time()
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    # hacemos el computo
    y = np.zeros(len(data))
    y = np.array(y, dtype=np.int16)
    
    for i in range(len(data)):
        M = 1+delay*RATE + delay *RATE* lfo[i]
        Mi = int(M)
        frac = M-Mi
        #y[i] = data[i -(Mi+1)]*frac + data[i-(Mi)]*(1-frac)
        if (i < (Mi+1)):
            y[i] = (data[i-Mi+1]*frac) + (data[i-Mi]* (abs(1-frac)))
        else:
            y[i] = data[i]
    #samples = y.astype(np.int16).tostring()
    if c == 30:
        print(' tiempo real flanger: ', time.time() - s)
    return (y, pyaudio.paContinue)

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
