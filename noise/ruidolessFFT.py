# ruidi con FFT
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft #, fftfreq
#from scipy.signal import hann

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
# read wave file
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)
print ('data ', data)

# ejecutando el algoritmo
#denoise = noise_reduction_fft(data)
N = len(data)
#t = np.arange(N/fs)#/fs

fft_data= fft(data,N)                   # compute the FFT
fftabs = abs(fft_data)

PSD = fft_data * np.conj(fft_data) / N  # Power spectral

freq = 1/fs*np.arange(N)            # create un z-axis of frequencies

L = np.arange(1, np.floor(N/2), dtype = 'int') # only plot the first half
#PSD0 = np.where(PSD<5000, 0, PSD)

indices = PSD > 50000  # finf all frequencies with large power
filtered = fft_data*indices
filt = ifft(filtered)

#freqs = fftfreq(len(data), 1/fs)
#fft_freqs = np.array(freqs)
#freqs_side = freqs[range(N//2)] # one side frequency range
#fft_freqs_side = np.array(freqs_side)

# salida
# write wav file
try:
    wavfile.write('/home/pi/wavfiles/ruidolessFFT.wav',
                      fs, filt.real.astype(np.int16))                  
                       #fs, y.real.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

# plot 
time = np.arange(len(data))/fs
L = np.arange(1, np.floor(N/2), dtype = 'int') # only plot the first half

plt.figure(1)
plt.plot(time[L], PSD[L], color = 'k', label = 'Señal con ruido')
plt.axhline(50000, ls = '--', c='r')
plt.ylim(0, 70000)
plt.legend()
plt.title("_PSD_ con ruido")
plt.xlabel('frecuencia')
plt.ylabel('magnitud')
plt.grid(True)
plt.tight_layout()

plt.figure(2)
plt.plot(time[L], filtered[L], color = 'b', label = 'Señal sin ruido')
plt.axhline(50000, ls = '--', c='r')
plt.ylim(0, 70000)
plt.legend()
plt.title("_PSD_ sin ruido")
plt.xlabel('frecuencia')
plt.ylabel('magnitud')
plt.grid(True)
plt.tight_layout()
plt.show()
