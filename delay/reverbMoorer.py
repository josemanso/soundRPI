# Moorer reverberation
import sys
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter
import matplotlib.pyplot as plt


# 6 Filtros low-pass peine paralelos que simularán los
# sonidos reflejados entre las paredes de una habitación 

# allpass filters para la difusión

# lowpass filters insertados en los bucles feedback(fidfusión)

# lowpass comb filter
def lpcomb(x, g, g1, delay):
    # Feedback comb filter con un lowpass filter en el
    # x = input
    # d = delay
    # g1 = 0.5*ones(1,6)
    # cg = g2./(1-g1);  g
    ## las ganancias han de ser menores que 1
    if g >= 1:
        g = 0.7
    if g1 >= 1:
        g1 = 0.7
    y = np.zeros(len(x))
    for i in range(len(x)):
        y[i] = g*x[i] + g1 *y[i-delay]
    
    return y
# all pass
def allpass(x, g, d):
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


def moorer(x, cg, cg1, cd, ag,ad):
    # x input
    # cg = vector long 6  g2/(1-g1) <1
    #      g2 es feedback gain
    # cg1 = vector long 6 gain low pass filter in feedback loop
    #        <1 para ser estable
    # 
    # cd = vector de long6 delay of each comb filter
    # ag = gain all pass filter <1
    # ad = delay of all pass filter
    # y = the output signal
    # b = the numerator coefficients of transfer function
    # a = the denominator coeficients of the transfer fuction
    
    # input to each of the 6 comb filters

    comb1 = lpcomb(x, cg[0], cg1[0], cd[0])
    comb2 = lpcomb(x, cg[1], cg1[1], cd[1])
    comb3 = lpcomb(x, cg[2], cg1[2], cd[2])
    comb4 = lpcomb(x, cg[3], cg1[3], cd[3])
    comb5 = lpcomb(x, cg[4], cg1[4], cd[4])
    comb6 = lpcomb(x, cg[5], cg1[5], cd[5])
    
    apinput = comb1 +comb2+comb3+comb4+comb5+comb6
    apinput = apinput/6
    
    yallpass = allpass(apinput, ag, ad)
    
    return yallpass
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
    #filename ="/home/josemo/"+file_input
    print('file exit')
else:
    print('File not exit')
    exit()


# read wave file
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)
print ('data ', data)

# algotirmo Moorer
# delay de cada comb filter
# delay de cada allpass filter

# generamos 6 retardos aleatorios
cd = np.random.randint(1,9,size=6)
for i in range(len(cd)):
    cd[i] = int(cd[i]*0.05*fs)
# ganacias de los 6 comb pass filters
g11 = np.ones(6)
for i in range(len(g11)):
    g11[i] = 0.6
# feedback
g12 = np.ones(6)
for i in range(len(g11)):
    g12[i] = 0.6
    
# set input cg and cg1 for moorer function see help moorer
cg = g12/(1-g11)
cg1 = g11
# ganancias all pass
ag = 0.7
# delay of all pass filter
ad = int(0.08*fs)

# señal directa, ganancia
k = 0.5

y = moorer(data, cg, cg1, cd, ag, ad)
# añadimos la señal
y = y + k*data

# write wav file
try:
    wavfile.write('/home/pi/wavfiles/reverb1.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

#plot
time = np.arange(len(data))/fs
plt.plot(time, y, 'r--',time, data,'g--')
plt.title("Moorer's Reverb")
plt.xlabel('Original green, reverb red')
plt.show()
       
    
    

