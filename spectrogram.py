# espectrograma
import sys
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft, spectrogram
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
    
# lectura del archivo .wav
fs, audio = wavfile.read(filename)

#nperseg =1025
#noverlap = nperseg-1
f, t, Sxx = spectrogram(audio,fs, window = 'hamming', nperseg =256)

print('f.shape ', f.shape)
print('t.shape ',t.shape)
print('Sxx.shape ', Sxx.shape)

plt.pcolormesh(1000*t, f/1000, 10*np.log10(Sxx/Sxx.max()))
plt.ylabel('frequency (kHz)')
plt.xlabel('Time (ms)')
#plt.pause(0.005)
plt.colorbar()
           
plt.show()

