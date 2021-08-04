# conlvolve reverberation
import sys
import os
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt
import time

# Reverberación por comvolución

def fconv(x,h):
    ly = len(x)+len(h) -1
   
    X = fft(x, ly)
    H = fft(h, ly)
    
    Y = X * H  # convolution
    y = np.real(ifft(Y,ly))
    y=y/max(abs(y))
    return y

# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "guitar.wav"
        #file_input_rir = "church.wav"
        
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
except IOError as ex:
    print(ex)
# excepcion de fichero
if os.path.isfile("/home/pi/wavfiles/"+file_input):
    filename ="/home/pi/wavfiles/"+file_input
    #filename_rir ="/home/pi/"+file_input
    print('file exit')
else:
    print('File not exit')
    exit()

# read wave file
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)
#print ('data ', data)

# tomamos el archivo de respuesta a impulso
fsIr, IR = wavfile.read("/home/pi/wavfiles/IR/church.wav")
print('data IR ', IR.shape, ' fs ', fsIr)

tr = np.arange(len(IR))/fsIr
plt.figure(1)
plt.plot(tr, IR)
plt.title('Impulse response')
# tiempo
start = time.time()
# normalizamos entre -1 y 1
datan = data/2**15
IRn = IR/2**15
# convolución
yout = fconv(datan,IR)

yout = yout * 2**15
print(' Convolución tiempo de procesado: ', time.time() - start)
# write wav file
try:
    wavfile.write('/home/pi/wavfiles/reverbConvchur2.wav',
                       fs, yout.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

#plot
plt.figure(2)
time = np.arange(len(data))/fs
plt.subplot(211)
timerv= np.arange(len(yout))/fs
plt.plot(timerv, yout)

plt.title("Convolution Reverb")
plt.xlabel('reverberation ')

plt.subplot(212)
plt.plot(time, data)
plt.xlabel("origin")


plt.show()