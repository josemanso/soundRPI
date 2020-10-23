# inpulse response FIR, g = 0.8, delay 10--12
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# Inpulse response a = 0.8, delay 15
# inpulso
I = np.zeros(120)
I[0] = 1
# coeficientes b
bi = np.zeros(120)
bi[0] = 1
bi[15] = 0.8
bi[30] = 0.6 # mayor atenuación
bi[45] = 0.4
bi[60] = 0.2
bi[75] = 0.1

impulse_response = lfilter(bi, 1, I)

plt.plot(impulse_response)
plt.title('Respuesta impulso FIR')
plt.xlabel('a = 1, b = [1,0,..,0.8,...,0.6,0,0...]')
plt.show()