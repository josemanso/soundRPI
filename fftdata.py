# Dominio de frecuencias; FFT
import sys
import os
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq, rfft
import matplotlib.pyplot as plt

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
    
# lectura del archivo .wav
fs, audio = wavfile.read(filename)

# FFT
datafft = fft(audio)
# abs
fftabs = np.abs(datafft)
freqs = fftfreq(len(audio), 1/fs)

#  plot
plt.figure(1)
plt.title('FFT')
plt.xlim([10, fs/2])
plt.xscale('log')
plt.grid(True)
plt.xlabel('Frecuencia, Hz')
plt.ylabel('Magnitud')
plt.plot(freqs[:int(freqs.size/2)], fftabs[:int(freqs.size/2)])


plt.figure(2)
fft_rfft = abs(rfft(audio))
fft_db = 20 * np.log10(fft_rfft)
# normalise to 0 db max
fft_db  -= max(fft_db)
plt.xscale('log')
plt.plot(freqs[:int(freqs.size/2)], fft_db[:int(freqs.size/2)])
plt.title('FFT - dB')
plt.xlabel('frecuencia, Hz')
plt.ylabel('Magnitus, (dB)')
plt.grid(True)

plt.show()

