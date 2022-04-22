# Schroeder reverberator
import sys
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import time

# 4 IIR comb filter, en paralelo
# cocetados a dos allpas

def comb(x,g,d):
    # x input
    # g gain feedback
    # d delay
    y = np.zeros(len(x))
    y[:d] = x[:d]
    for i in range(d,len(x)):
        y[i] = x[i] + g * y[i-d]
    return y
def allpass(x,g,d):
    # x input
    # g gain feedback/feedforward
    # d delay
    y = np.zeros(len(x))
    y[:d] = x[:d]
    for i in range(d,len(x)):
        y[i] = g*x[i] + x[i-d] - g*y[i-d]
    return y

def schroeder(x, fs):
    # comb 1  g = 0.742 ; 29,7 ms ;4799; 
    # comb 2  g = 0.733 ; 37,1   delay = 4999
    # comb 3  g = 0.715 ; 42,1 delay time = 5399
    # comb 4  g = 0.697 ; 43,7 delay time = 5801
    mult = fs* 10**-3
    comb1 = comb(x, 0.742, int(mult*29.7))
    comb2 = comb(x, 0.733, int(mult*37.1))
    comb3 = comb(x, 0.715, int(mult*41.1))
    comb4 = comb(x, 0.697, int(mult*43.7))
    
    comb_out = (comb1 + comb2 + comb3 + comb4) / 3
    
    # all-pass1 gain = 0.7, delay time = 5  ;1051
    # all-pass2 gain = 0.7, delay time = 1,7 ;337
    y1 = allpass(comb_out, 0.7, int(mult*5))
    y2 = allpass(y1, 0.7, int(mult*1.7))
    
    return y2

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
    #filename ="/home/josemo/"+file_input
    print('file exit')
else:
    print('File not exit')
    exit()


# read wave file
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)
print ('data ', data)
#tiempo
start = time.time()
yout = schroeder(data, fs)
#yout = schroeder(data[fs:], fs)
print(' tiempo Schroeder reverb: ', time.time() - start)
# write wav file
try:
    wavfile.write('/home/pi/wavfiles/reverbSch.wav',
                       fs, yout.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

#plot
time = np.arange(len(data))/fs
plt.plot(time, yout, 'r--',time, data,'g--')
plt.title("Reverberación, Schroeder")
plt.xlabel('Original green, reverb red')
plt.xlabel('Tiempo(s): Señal original, verde; reverb. rojo')
plt.ylabel('Amplitud')
plt.grid(True)
plt.tight_layout()
plt.show()

    
    
        
    