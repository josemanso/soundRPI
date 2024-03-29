#ecualizador graves y agudos tiempo real
import numpy as np
import pyaudio
import time
from scipy.signal import lfilter

from shelvingFunction import shelving

# dispositivo de entrada / salida
dev_index = 2 # device index found by p.get_device_info

G_base = 5
G_trev = -5
fclow = 200
fchigh = 3000
Q = 0.7

RATE = 44100

def gaincontrol(G, G1, Q, fcl, fch, data):
    if G == 0:
        y_base = data
        bt, at = shelving(G1,fcl,fch,Q, tipo= 'Treble_Shelf')
        y_treble = lfilter(bt,at,data)
    elif G1 ==0:
        bb, ab = shelving(G,fcl,fch,Q, tipo= 'Base_Shelf')
        y_base = lfilter(bb,ab,data)
        y_treble = data
    else:
        bb, ab = shelving(G,fcl,fch,Q, tipo= 'Base_Shelf')
        bt, at = shelving(G1,fcl,fch,Q, tipo= 'Treble_Shelf')
        y_base = lfilter(bb,ab,data)
        y_treble = lfilter(bt,at,data)
    
    y_gc = y_base + y_treble
    y_gc /= 2.3 # y_gc/2.3
    return y_gc


pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # tiempo
    c = np.random.randint(100)
    if c == 30:
        s = time.time()
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    
    y = gaincontrol(G_base, G_trev, Q, fclow, fchigh, data)

    
    sample = y.astype(np.int16).tostring()
    if c == 30:
        print('tiempo graves agudo: ', time.time() - s)
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