# wah peak filter
import sys
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import iirpeak 
import matplotlib.pyplot as plt
import time

# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "guitar.wav"
        
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


# read wave file
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)


# creamos un LFO para variar la frecuencia de corte.
cut_min = 500    # LFO minval, Hz
cut_max = 3000   # LFO maxval, Hz
fw =  2000       # wah frecuency,
# cetro de la frecuencia
delta = fw/fs

depth = 2   # factor Q, filter iirpeak fw/fs

# crear una onda triangular con los valores de frecuencias
fc = []
while (len(fc)<len(data)):
    fc = np.append(fc, np.arange(cut_min, cut_max, delta))
    fc = np.append(fc, np.arange(cut_max, cut_min, -delta))
# quitamos lo qe sobra
fc = fc[:len(data)]

y = np.zeros(len(data))
start = time.time()
for i in range(2,len(data)):
    b, a = iirpeak(fc[i]/(fs/2), depth)
    y[i] = (b[0]*data[i] + b[1]*data[i-1]+ b[2]*data[i-2]
            -a[1]*y[i-1]-a[2]*y[i-2])
            
gain = 0.8

yout = (1-gain)*data +  gain*y
print('tiempo filtrado iirpeak wah-wah: ', time.time() - start)
# write wav file
try:
    wavfile.write('/home/pi/wavfiles/wahwah.wav',
                       fs, yout.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)
    

#plot
timel = np.arange(len(data))/fs
plt.figure(1)

plt.plot(timel,data, 'g--', timel, yout,'r--')
#plt.plot(time, lfo)
plt.title('Efecto wah-wah')
plt.xlabel('señal original verde, señal filtrada rojo')
plt.figure(2)
plt.plot(timel, fc)
plt.title('LFO, para el efecto wah-wah')
plt.show()