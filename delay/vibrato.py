# Vibrato effect
import sys
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# entrada de argumentos
try:
    if len(sys.argv) == 1:
       file_input = "acoustic.wav"
        
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

# read wave file
fs, data = wavfile.read(filename)
print('fs ', fs, 'data shape ', data.shape)

# tipical delay, entre 5 y 10ms, LFO entre 5 y 14 Hz
#delay = 0.010  # 8  ms
delay = 0.0005

rate = 10  # Hz

y = np.zeros(len(data))

#maxdelay = math.ceil(1+delay*fs+1)

for i in range(len(data)):
    M = 1+delay*fs+delay*fs*np.sin(rate/fs*2*np.pi*i)
    #M = 1+delay*fs+delay*fs*np.sin(rate*2*np.pi*i)
    Mi = int(M)
    frac = M - Mi
    # primeros retardos han de ser positivos
    if (Mi + 1)  > i:
        Mi = i-1
    #y[i] = data[i -(Mi+1)]*frac + data[i-(Mi-1)]*(1-frac)
    y[i] = data[i -(Mi+1)]*frac + data[i-(Mi)]* abs(1-frac)
                                       
# write wav file
try:
    wavfile.write('/home/pi/wavfiles/vibrato1.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)  
#plot
#f, ax1 = plt.subplots(1,1,figsize=(8,5))
plt.figure(figsize=(8,5))
time = np.arange(len(data))/fs
plt.plot(time, data,'g--',time, y, 'r--')
plt.title('Vibrato')
plt.xlabel('Rojo datos vibrato, verde, audio original')
#plt.figure(2)
#plt.plot(y)
#lfo1 = delay*fs*np.sin(rate/fs*2*np.pi*time)# cuanto más grande maveces cambia, frecuencia
#plt.figure(3)
#plt.plot(lfo1)
#ax1[1].plot(time, data, 'g--', time, data1, 'r--')
plt.show()
             