# reverb realtime
import numpy as np
import pyaudio
import time


RATE = 44100
# dispositivo de entrada / salida
dev_index = 2 # device index found by p.get_device_info
# delay < 50 ms  50 *44,2 == 2205 y / 1024 = 2,15  - 3
#M = 1764 # delay 40 ms, solo necesito dos
M= 2200 # mejor
#M = 1500 # delay 32 ms, solo necesito dos
# con arrays
a = 3072 # 1024 x 3,
b = 4096 # 3072 +  + 1024 desde el siguiente
A = np.array([]) # entrada
B = np.array([]) # salida

g = 0.5
y = np.zeros(1024)

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # tiempo
    c = np.random.randint(100)
    if c == 30:
        s = time.time()
    # convert data to array
    data = np.frombuffer(in_data, np.int16)

    global A, B, y
    # almacenamos 3 chunks x 1024
    A = np.append(A, data)
   
    if len(A) == b: #a +1024:
        if len(B) == 0:
            B = A # salida inicial
        # hacemos ya el computo
        for i in range(len(data)):
            y[i] = -g * data[i] + A[i+a-M] + g*B[i+a-M]
            #y = y/2
        # actualizamos almacen
        B = B[1024:]
        A = A[1024:]
        B = np.append(B, y)

    samples = y.astype(np.int16).tostring()
    #if c == 30:
        #print('tiempo reverb: ', time.time() - s)
    return (samples, pyaudio.paContinue)

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
    time.sleep(20)
    stream.stop_stream()
    print("Stream is stopped")

stream.stop_stream()
stream.close()

pa.terminate()