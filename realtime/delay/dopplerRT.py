#doppler realtime
import numpy as np
import pyaudio
import time

#import matplotlib.pyplot as plt

RATE = 44100
# 5 segundos; rate 44100 x 5 = 220500 tramas ;216 x 1024 =221184
dev_index = 2 # device index found by p.get_device_info

seg = 5

L = seg * RATE #133120 

times = np.arange(L)/RATE
velocity  = 70.0 # velocidad de la fuente 
Vsonido = 342.0 # m/seg

# posición
# vector x  = espacio x tiempo
x = times * velocity
# lo dividimos por la mitad, una parte negativa y otra positiva
x -= x.max()/2.0

# vector y
y = np.zeros(L)
# z
z = 100.0 * np.ones(L)

position_source = np.vstack((x,y,z)).T # columnas
position_receiver = np.zeros(3)

distance = np.linalg.norm((position_source-position_receiver), axis = 1)

delay = distance / Vsonido

# aumentar disminuir. para invertir la curva delay
aumentar = np.linspace(-max(delay), 1, L//2)
disminuir = aumentar[::-1]
aux = np.concatenate((aumentar, disminuir), axis=0)


gain = np.ones(L)

for h in range(0, L):
    gain[h] = delay[h] + aux[h]
   
pa= pyaudio.PyAudio()

indice = 0
def callback(in_data, frame_count, time_info, status):
    c = np.random.randint(100)
    if c == 30:
        s = time.time()
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    data = data.copy()
    # hacemos el computo
    global indice
    for i in range(len(data)):
        data[i] = data[i] * gain[indice]
        indice +=1
        if indice >= L:
            indice = 0
    #samples = y_f.astype(np.float64).tostring()
    if c == 30:
        print(' tiempo real doppler: ', time.time() - s)
    return (data, pyaudio.paContinue)


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
    time.sleep(12)
    stream.stop_stream()
    print("Stream is stopped")

stream.stop_stream()
stream.close()

pa.terminate()
"""
plt.subplot(211)
plt.plot(times,delay)
plt.xlabel('delay')
plt.subplot(212)
plt.plot(gain)
plt.xlabel('gain')
plt.show()
"""