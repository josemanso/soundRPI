
# impulse response all-pass

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# Impulse response a = 0.8, delay = 20
I = np.zeros(120)
y = np.zeros(120)
I[0] = 1
a = 0.9
D = 20

bi = np.zeros(20)
bi[0] = 0 #bi[0] = -a
bi[-1] = a
ai = np.zeros(20)
ai[0] = 1
ai[-1] = -a # -0.8
# con filtro
#impulse_response = lfilter(bi, ai, I)

# con función
for i in range(20,120):
    y[i] = -a*I[i] + I[i-D] + a*y[i-D]
#plt.figure(2)
#plt.plot(impulse_response)
plt.plot(y)
plt.title('Respuesta Impulso all-pass')
plt.xlabel('b = [0,0...,a] y a=[1, 0,...,-a]')
plt.show()
