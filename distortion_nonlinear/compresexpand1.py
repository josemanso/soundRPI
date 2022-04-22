# Compressor Expander
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import time

def comprexpander(x, ratio, th_compress, th_expan):
    # x data input
    # ratio  ratio conpressor 1/ratio, expander ratio
    # th  threshold
    
    # para comparar con los valores de los datos 
    th_c = 10**(th_compress/20)*32769
    th_e = 10**(th_expan/20)*32769
    
    cn = np.zeros(len(x)) # detección de nivel
    gain = np.ones(len(x)) # ganacia
    gain_c = np.ones(len(x))# show gain comp
    gain_e = np.ones(len(x))# show gain exp
    out = np.zeros(len(x))
    out[0] = x[0]
    cn[0] = abs(x[0])
    for i in range(1,len(x)):
        cn[i] = abs(x[i])
        if abs(x[i]) > th_c:
            # compresión
            if cn[i] > cn[i-1] :
                #cn[i] = t_ata * cn[i-1] + (1- t_ata)*abs(x[i])
                cn[i] = cn[i] # esto ya está
            else:
                cn[i] = cn[i-1]
            # proceso de ganacia f[c]   
            gain[i] =(cn[i] / th_c)**(1/ratio - 1)
            gain_c[i] = gain[i]
            # si no la ganacia queda a 1
        elif abs(x[i]) < th_e :
            # expansor si es mayor que el ruido
            if (abs(x[i]) > 10) :
                gain[i] = 1/(cn[i] / th_e)**(ratio -1)
                gain_e[i] = gain[i]
            else:
                gain[i] = 0
                gain_e[i] = gain[i]
                
                # sino queda a 1
        else:
            gain[i] = 1
        # fin del proceso de ganacias
        #plt.plot(cn)
        #plt.show()
        out[i] = x[i] * gain[i]
    #plt.plot(gain)#[:4000])
    #plt.show()
    return out, gain, gain_c, gain_e
    #return out
# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "fish.wav"
        
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
except IOError as ex:
    print(ex)
# excepcion de fichero
# excepcion de fichero
if os.path.isfile("/home/pi/wavfiles/"+file_input):
    filename ="/home/pi/wavfiles/"+file_input
    print('file exit')
else:
    print('File not exit')
    exit()
fs, data = wavfile.read(filename)
print('data ', data.shape, ' fs ', fs)

th_comp= -10#-5 # dB
th_exp = -60#-70 # dB
CR = 4
# tiempo
start = time.time()
#y = comprexpander(data, CR, th_comp, th_exp)
#print('tiempo de fitrado compresor: ', time.time() - start)
y, g, gc, ge = comprexpander(data, CR, th_comp, th_exp)
print('tiempo de fitrado compresor: ', time.time() - start)
# write wav file
try:
    wavfile.write('/home/pi/wavfiles/comprexpander1.wav',
                       fs, y.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)

#plot
timel = np.arange(len(data))/fs
plt.figure(1)
#plt.subplot(211)
plt.plot(timel, y, 'r--', timel, data,'g--')
plt.xlabel('Señal original verde, señal comprimida /espandida, rojo')
#plt.subplot(212)
plt.figure(2)
# máx alrededor de 3.6, antes

plt.plot(timel,data, 'g--',timel,y, 'r--')
plt.title('Compresor/Expansor')
plt.xlabel('tiempo (s)')
plt.ylabel('amplitud')
plt.grid(True)
plt.tight_layout()
#plt.xlabel('Señal original verde, señal comprimida /espandida, rojo')
#plt.ylabel("log")
plt.figure(3)
plt.plot(timel,g)
plt.xlabel('ganancia')
plt.figure(4)
plt.plot(timel,gc)
plt.title('compresión')
plt.xlabel('tiempo (s)')
plt.ylabel('ganancia')
plt.grid(True)
plt.tight_layout()
#plt.xlabel('compresión')
plt.figure(5)
plt.plot(timel,ge)
plt.title('expansión')
plt.xlabel('tiempo (s)')
plt.ylabel('ganancia')
plt.grid(True)
plt.tight_layout()
#plt.xlabel(' expansión ')
#plt.grid()

#plt.figure(3)
#plt.plot(time,gain)
#plt.ylabel("log")
#plt.grid()


plt.show()




