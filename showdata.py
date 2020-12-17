import sys
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# entrada de argumentos
try:
    if len(sys.argv) == 1:
       file_input = 'grabacion1.wav'
       
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
except IOError as es:
    print(ex)
# excepción de fichero
if os.path.isfile("/home/pi/wavfiles/"+file_input):
    filename = "/home/pi/wavfiles/"+file_input
    print('file exit')
else:
    print('Fiele not exit')
    exit()
    
# lectura del archivo
fs, audio = wavfile.read(filename)
print('frecuencia: ', fs, ' Hz')
print('audioshape: ',audio.shape, ', array longitud \nlongitud: ',
      len(audio))
print('datos: \n', audio)

time = np.arange(len(audio))/fs
plt.plot(time, audio)
plt.title('Wave form')
plt.xlabel('time, seconds')
plt.ylabel('Amplitud')

plt.show()
