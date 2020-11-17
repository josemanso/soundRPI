# efecto doppler
import sys
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


# entrada de argumentos
try:
    if len(sys.argv) == 1:
        #file_input = "440Hz_44100Hz_16bit_05sec.wav"
        file_input = "CantinaBand60.wav"
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
#print(' fs', fs,' shapes ', data.shape, ' data ', data)
data= data[:15*fs] # acortamos a 5 segundos
print(' fs', fs,' shapes ', data.shape, ' data ', data)

L = len(data)
times = np.arange(L)/fs

velocity  = 70 # velocidad de la fuente 
Vsonido = 342.0 # m/seg

# posición
# vector x  = espacio x tiempo
x = times * velocity
# lo dividimos por la mitad, una parte negativa y otra positiva
x -= x.max()/2.0

# vector y
y = np.zeros(L)
# z
z = 100.0 * np.ones(L)

position_source = np.vstack((x,y,z)).T # columnas
position_receiver = np.zeros(3)

distance = np.linalg.norm((position_source-position_receiver), axis = 1)

delay = distance / Vsonido

# aumentar disminuir
aumentar = np.linspace(-max(delay), 1, L//2)
disminuir = aumentar[::-1]
aux = np.concatenate((aumentar, disminuir), axis=0)
# gains
gain = np.zeros(L)
yout = np.zeros(L)

for i in range(L):
    gain[i] = delay[i] + aux[i]
    yout[i] = gain[i] * data[i] 

# write wav file
try:
    wavfile.write('/home/pi/wavfiles/doppler.wav',
                       fs, yout.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)      

#fig = plt.figure(1, figsize =(8,3))
#ax = fig .add_subplot(1,2,1)
plt.figure(1)
plt.subplot(2,1,1)
#plt.plot(data, 'g--', yout, 'r--')
plt.plot(times, yout)

plt.title('Efecto doppler')
plt.subplot(2,1,2)
plt.ylabel('delay')
plt.plot(times, delay)
plt.xlabel('segundos')
plt.figure(2)
plt.ylabel('gain')
plt.plot(times, gain)
plt.xlabel('segundos')
plt.show()
