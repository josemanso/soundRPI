
# ecualizador graves agudos, filtros shelving
import sys
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import matplotlib.pyplot as plt
import time

from shelvingFunction import shelving

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
    
    print('file exit')
else:
    print('File not exit')
    exit()


# read wave file
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)


# filtro Shelving de 2º orden
# set Parameters for Shelving Filter 
G = -5
G1 = 5
fcl = 200
fch = 3000
Q = 0.7
#tipo = 'Base_Shelf'  'Treble_Shelf'
fs = 44100

bb, ab = shelving(G, fcl, fs, Q, tipo = 'Base_Shelf')
bh, ah = shelving(G1, fch, fs, Q, tipo = 'Treble_Shelf')

# en serie
graves = lfilter(bb,ab, data)
agudos = lfilter(bh,ah, data)
# tiempo
start = time.time()
y = graves+agudos
y[y>32768] = 32767
y[y<-32768] = -32767

y = y/2
print('tiempo de fitrado graves y agudos: ', time.time() - start)
# write wav file
try:
    wavfile.write('/home/pi/wavfiles/ecualiGravesAgudos.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)
# write wav file

#plot
#f, ax1 = plt.subplots(2,1,figsize=(5,5))
timel = np.arange(len(data))/fs
plt.plot(timel, data,'g--',timel, y, 'r--')#,time, data,'g--')
plt.title('Ecualizador grave y agudos')
plt.xlabel('Original green, ecualizada red')
plt.show()
