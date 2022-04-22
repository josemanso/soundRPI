# distorsión fuzz
import numpy as np
import pyaudio
import time

# dispositivo de entrada / salida
dev_index = 2 # device index found by p.get_device_info
norm = 32768  # de int16 a valores entre -1 y 1
gain = 2 # ganancia gain
def distorfuzz(x, g):         
    q = x *g
    y = np.sign(-q)*(1-np.exp(np.sign(-q)*q))
    
    return y

RATE = 44100

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # tiempo
    c = np.random.randint(100)
    if c == 30:
        s = time.time()
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    data1 = data.copy()
    # hacemos el computo
    data1 = data1/ norm # valores entre 1 y -1
    #data1 /= 32768
    y_out = distorfuzz(data1, gain)
    y_out *= norm
    
    sample = y_out.astype(np.int16).tostring()
    #return (in_data, pyaudio.paContinue)
    if c == 30:
        print('tiempo distorsión: ', time.time() - s)
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