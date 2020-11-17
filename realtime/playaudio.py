import os
import pyaudio
import time

import numpy 

#WIDTH = 2
#CHUNK = 1024
RATE = 44100


pa = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # convert data to array
    data = numpy.frombuffer(in_data, numpy.int16)
    return (data, pyaudio.paContinue)

stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate = RATE,
                 input=True,
                 output=True,
                 stream_callback=callback)

stream.start_stream()

try:
    while stream.is_active():
        time.sleep(10)
        stream.stop_stream()
        print("Stream is stopped")
except os.error as ex:
    print(ex)
    
stream.close()

pa.terminate