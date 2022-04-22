# ecualizador de bandas; respuesta impulso
import sys
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter, freqz
import matplotlib.pyplot as plt

from shelvingFunction import shelving
from peakFunction import peakfilter

fs = 44100
Q = 0.7
# b,a = peakfilter(gain, fc,fs,Q) 
bp1,ap1 = peakfilter(1, 180,fs,Q)
w1, h1 = freqz(bp1, ap1, fs)
freq1 = w1*fs/(2*np.pi)
bp2,ap2 = peakfilter(1, 540,fs,Q)
w2, h2 = freqz(bp2, ap2, fs)
freq2 = w2*fs/(2*np.pi)
bp3,ap3 = peakfilter(1, 1620,fs,Q)
w3, h3 = freqz(bp3, ap3, fs)
freq3 = w3*fs/(2*np.pi)
bp4,ap4 = peakfilter(1, 4860,fs,Q)
w4, h4 = freqz(bp4, ap4, fs)
freq4 = w4*fs/(2*np.pi)

# llamada a la función shelving
bsg, asg = shelving(1, 100, fs, Q, tipo = 'Base_Shelf')
wsg, hsg = freqz(bsg, asg)
freqsg = wsg*fs/(2*np.pi)
bsa, asa = shelving(1, 8000, fs, Q, tipo = 'Treble_Shelf')
wsa, hsa = freqz(bsa, asa)
freqsa = wsa*fs/(2*np.pi)

# plot
fig, ax =plt.subplots()
#ax.plot(freq, 20*np.log10(abs(h)), 'g--', label='1000')
ax.plot(freqsg, abs(hsg), 'p--', label='100')

ax.plot(freq1, abs(h1), 'r--', label='180')
ax.plot(freq2, abs(h2), 'g--', label='540')
ax.plot(freq3, abs(h3), 'b--', label='1620')
ax.plot(freq4, abs(h4), 'y--', label='4860')

ax.plot(freqsa, abs(hsa), 's--', label='8000')

plt.title('Equalizador paramétrico, con filtros shelving y peak')
plt.yscale("log")
plt.xscale("log")
plt.legend()
plt.xlabel('frecuencia')
plt.ylabel('amplitud/ganancia')
plt.grid()
plt.show()

