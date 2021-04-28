#ring Modulation
import sys
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "fish.wav"
        
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
#print ('data ', data)

#time = np.arange(len(data))/fs
index = np.arange(0, len(data), 1)
#print('index ', index)

# Ring Modulate with a sine wave frequency Fc
fc = 200 #600 #200#2
carrier = np.sin(2*np.pi*index*(fc/fs))

y = carrier * data

# write wav file
try:
    wavfile.write('/home/pi/wavfiles/ring.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

#plot
#f, ax1 = plt.subplots(2,1,figsize=(5,5))
time = np.arange(len(data))/fs
time2 = time[:1024]
#plt.plot(time, data,'g--',time, y, 'r--')
plt.plot(data[:1024],'g--', y[:1024], 'r--')
plt.title('Ring Modulation')
plt.xlabel('Original green, ring red')
plt.show()