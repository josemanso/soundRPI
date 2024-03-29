# Fuzz
# distortion based on an exponential function
import sys
import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import time

def distorfuzz(x, g):         
    q = x *g
    y = np.sign(-q)*(1-np.exp(np.sign(-q)*q))
    
    return y

# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "guitar.wav"
        
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
except IOError as ex:
    print(ex)
# excepcion de fichero
if os.path.isfile("/home/pi/wavfiles/"+file_input):
    filename ="/home/pi/wavfiles/"+file_input
   
    print('file exit')
else:
    print('File not exit')
    exit()

# read wave file
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)
print ('data ', data)

# normalizemos el data, lo hacemos valer entre 1 y -1
# nosotros tenemos valores de int16 osea 2¹⁶  / 2(positivos negativos)
# 65536 / 2 = 32768
norm = 32768

datan = data/norm
print('datann ', datan.shape, ' fs ', fs)
print('nor ', datan)
# tiempo
start = time.time()
y = np.zeros(len(datan))
g = 2 # ganancia
y = distorfuzz(datan,g)

# lo ponemos a 16 bits
y = y*32767
print('tiempo de fitrado distorsión: ', time.time() - start)

# write wav file
try:
    wavfile.write('/home/pi/wavfiles/distorsionfuzz.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

# onda sinuidal
fss = 100
t = np.arange(fss)
p = np.sin(2*np.pi*2*t/fss)
#p = np.sin(t)
z = distorfuzz(p, g)
#plot
timel = np.arange(len(data))/fs
plt.figure(2)
#plt.plot(time, data,'g--', time, y, 'r--')
plt.plot(timel, y,'r--', timel, data, 'g--')
plt.title("Distorsión Fuzz")
plt.xlabel('Tiempo (s); Señal original verde, overdrive rojo')
plt.ylabel('Amplitud')

f, ax = plt.subplots()
ax.plot(t,p, 'g', label='Original')
ax.plot(t,z,'r--',label='distor/fuzz')
ax.legend(loc='upper right')
plt.title('Distorsión/Fuzz sobre señal senoidal')
plt.xlabel('tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.tight_layout()
plt.show()
