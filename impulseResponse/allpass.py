# all pass filter
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

def allpass(x,g,d):
    # x input
    # g = the feedforward / feedback gain
    # d = delay
    
    # las ganancias han de ser menores que 1
    if g >= 1:
        g = 0.7
    # coeficientes
    b = np.zeros(d)
    b[0] = g
    b[-1] = 1
    
    a = np.zeros(d)
    a[0] = 1
    a[-1] = g
    
    # filtramos
    y = lfilter(b,a,x)
    return y


I = np.zeros(120)
I[0] = 1
h = allpass(I, 0.7, 10)
#plot
plt.figure(1)
plt.plot(h)
#plt.axis([0, 50,-0.8, 1.1])
plt.xlabel('Time (samples)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()


    
