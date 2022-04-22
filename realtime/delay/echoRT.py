# eco
# -*- coding: utf-8 -*-
import os
import numpy as np
import pyaudio
import time
import queue as queue

# dispositivo de entrada / salida
dev_index = 2 # device index found by p.get_device_info
RATE = 44100
# 1024*25 = 25600
q = np.ndarray([])
q = queue.Queue(50)#25)

def callback(in_data, frame_count, tiem_info, status):
    data = np.frombuffer(in_data, np.int16)
    #esperamos un tiempo o un nº de frames 
    q.put(data)
    if q.full():
        cola = q.get()
        #print('cola ', cola.shape, ' long d', cola)
        cola = [x*0.4 for x in cola]
        data = data + cola  
        data = np.array(data, dtype='int16')
    return (data, pyaudio.paContinue)

    
p= pyaudio.PyAudio()
stream = p.open(format= p.get_format_from_width(2),# dos bytes
                channels=1,
                rate= RATE,
                #input=True,
                #output=True,
                input_device_index = dev_index,input = True,
                output_device_index = dev_index,output = True,
                stream_callback =callback)

stream.start_stream()

try:
    while stream.is_active():
        print("Stream is active")
        time.sleep(10)
        stream.stop_stream()
        print("Stream is stopped")
except os.error as ex:
    print(ex)
    
stream.close()
p.terminate()
