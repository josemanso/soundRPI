# Eco
import sys
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "grabacion.wav"
        
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
except IOError as ex:
    print(ex)
# excepcion de fichero
if os.path.isfile("/home/pi/wavfiles/"+file_input):
    filename ="/home/pi/wavfiles/"+file_input
    #filename ="/home/josemo/"+file_input
    print('file exit')
else:
    print('File not exit')
    exit()
    
#
# IIR filter generate an infinite number of echoes with a = 0.8 for delay R =1000
#read wav file
fs, audio = wavfile.read(filename)

# retardo > 50 ms  , 44100 Hz c/s * 50 10e-3= 2205 samples
M = 30000# 50000 # samples delay, un segundo 0,6 seg.
#b = np.zeros(int(M/2))
b = np.zeros(1)
b[0] = 1

a = np.zeros(M)
a[0] = 1
a[-1] = -0.4

# iir
data_filt = lfilter(b,a,audio)

# write wav file
wavfile.write('/home/pi/wavfiles/eco.wav',fs,
              data_filt.astype(np.int16))
fs, data_eco = wavfile.read('/home/pi/wavfiles/eco.wav')

plt.figure()
plt.title('Echo IIR')
plt.plot(data_eco, 'r--', audio,'g--')
plt.xlabel('Original soun, green; data_filter, red')


plt.show()
