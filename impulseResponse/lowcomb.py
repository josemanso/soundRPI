# low pass comb filter
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt



I = np.zeros(120)
I[0] = 1

d = 20
gf = 0.5 # feedback 
gl = 0.3 # ganancia entrada

y = np.zeros(120)
for i in range(120):
    #y[i] = g1*I[i] + g *y[i-d]
    y[i] = gl*I[i] + gf *y[i-d]

plt.figure(1)
#plt.plot(impulse_response)
plt.title('Respuesta Impulso comb lowpas filter')
plt.xlabel('delay 10, ganancias 0.5 feedback y 0.3 low pass')
#plt.figure(2)
plt.plot(y)
plt.show()
