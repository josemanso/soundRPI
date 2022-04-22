# Respuesta impulso IIR
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# impulso
I = np.zeros(120)
I[0] = 1

# # parametros a y b
bi = np.zeros(20)
bi[0] = 1

ai = np.zeros(20)
ai[0] = 1
ai[-1] = -1#-0.8

impulse_response = lfilter(bi, ai, I)

plt.plot(impulse_response)
plt.title('Respuesta Impulso IIR')
plt.xlabel('Tramas: b = 1, a=[1, 0,...,-1]')
plt.ylabel('Amplitud')
#plt.grid(True)
plt.tight_layout()
plt.show()