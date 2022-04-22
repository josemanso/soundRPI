#ring Modulation
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# entrada de argumentos
try:
    if len(sys.argv) == 1:
        #file_input = "audio_sin_500Hz_10s.wav"
        file_input = "500Sine.wav"
        #file_input = "440Hz_44100Hz_16bit_05sec.wav"
        
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

#plot
#f, ax1 = plt.subplots(2,1,figsize=(5,5))
time = np.arange(len(data))/fs
#plt.plot(time, data,'g--',time, y, 'r--')
plt.plot(data[:1024],'g--', y[:1024], 'r--')
#plt.plot(data)
plt.title('Ring Modulation')

plt.xlabel('Muestras; Original, verde; ring rojo')
plt.ylabel('Amplitud')
plt.grid(True)
plt.tight_layout()
plt.show()