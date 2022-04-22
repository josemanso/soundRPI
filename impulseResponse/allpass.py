# all pass filter
import numpy as np
#from scipy.signal import lfilter
import matplotlib.pyplot as plt



I = np.zeros(120)
I[0] = 1
# x input
# g = the feedforward / feedback gain
# d = delay
d= 20
g = 0.9
y = np.zeros(120)
# con ecuación característica
for n in range (d, 120):
    y[n] = -g * I[n]+ I[n - d] +g *y[n - d]
#plot
plt.figure(1)
plt.plot(y)

plt.xlabel('Tiempo (tramas/samples)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.tight_layout()
plt.show()


    
