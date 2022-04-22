import os
import pyaudio
import time

import numpy 

#from error_hider import noalsaerr
#WIDTH = 2
#CHUNK = 1024
RATE = 44100

dev_index = 2 # device index found by p.get_device_info_by_index(ii)
pa = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = numpy.frombuffer(in_data, numpy.int16)
    return (data, pyaudio.paContinue)

stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate = RATE,
                 #input=True,
                 input_device_index = dev_index,input = True,
                 output_device_index = dev_index,output = True, 
                 #output=True,
                 stream_callback=callback)

stream.start_stream()

try:
    while stream.is_active():
        time.sleep(20)
        stream.stop_stream()
        print("Stream is stopped")
except os.error as ex:
    print(ex)
    
stream.close()

pa.terminate