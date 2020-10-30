import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

fs = 1000.0  # Sample frequency (Hz)
f0 = 300.0  # Frequency to be retained (Hz)
Q = 30.0  # Quality factor
# Design peak filter
b, a = signal.iirnotch(f0/(fs/2), Q)

# Frequency response
freq, h = signal.freqz(b, a)
# Plot
plt.plot(freq, 20*np.log10(np.maximum(abs(h), 1e-5)), color='blue')
plt.title("Frequency Response")
plt.xlabel('freq. ')
plt.ylabel('Amplitude, dB')
plt.show()