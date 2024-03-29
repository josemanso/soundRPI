#sustracción espectral
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
from scipy.signal import hann
import time
#The noisy signal y(m) is a sum of the desired signal
# x(m) and the noise n(m);  y(m) = x(m) + n(m)
# In the frequency domain, this may be denoted as:
# Y(jω) = X(jω) + N(jω)  =>  X(jω) = Y(jω) - N(jω)

def spectralSubtraction(data, f_size, n_frames, alpha):
    
    # data is the complete signal
    # f_size is the size of frames, nº points, windowing
    # n_frames is the number of noise frames
    # overlap 50%
    
    # samples stores a list of overloapped window of size f_size
    samples = []
    
    # phases stores a list phases information of every frames
    phases  =[]
    
    # y will be the final reconstruction signal
    y = np.zeros((len(data)), dtype='complex')
    
    # nº de ventanas que tendremos
    lps = int(len(data)/f_size) +1
    
    # Hann window
    hn_win = hann(f_size)
    
    for i in range(lps*2):
        
        # estract 50% overlapping frames of f_size of signal
        # and append to samples
        f_loc = int(i*f_size/2)
        samples.append(np.asarray(data[f_loc:f_loc+f_size]))
        
        # Apply Hann window, FFT,
        # save information in list phases
        # estract magnitude
        elem = len(samples) -1
        samples[elem] = samples[elem] * hn_win[:len(samples[elem])]
        samples[elem] = fft(samples[elem])
        phases.append(np.angle(samples[elem]))
        samples[elem] = abs(samples[elem])
        
        if (len(samples[elem]) < f_size):
            # sino hay tramas suficientes
            break
        
    # assuming first few frames are only noisy frames,
    # Sum all the noisy frames in one frame
    noise = np.asarray(samples[0])
    for j in range(1, n_frames):
        # sumamos arrays,
        # elemento a elemnto y nos quedamos con una
        noise = list(map(lambda x, y : x+y, noise, samples[j]))
        
    # Get an average noise magnitude
    noise = list(map(lambda x: x/n_frames, noise))
    noise = np.mean(noise) # ya tenemos un valor medio
    print('noise ', noise)    
    # multiply bia to noises, factor de aumento del ruido
    #noise *=7
    noise*=alpha
    #print('noise ', noise)
    
    
    
    # perform spectra subtraction
    samples = [list(map(lambda x : x - noise, i)) for i in samples]
    
    # perform half wave rectification
    for idx, frm in enumerate(samples):
        samples[idx] = [0 if i < noise else i for i in frm]
        
      
    # ahora hacemos la ifft
    # zero off negative amplitudes.
    # multuply phase information with their respectives frames.
    # Perform IFFT  
        
    for h in range(len(samples)-1):
        #samples[h][samples[h] <0 ] =0# [ 0 if i < 0 else i for i in samples]
        #np.where(samples[h] <0, 0, samples[h])
        #samples[h] = [0 if i < 0 else i for i in enumerate(samples[h])]
        samples[h] = [0 if i < 0 else i for i in (samples[h])]
        # formula de Euler
        samples[h] =list(map(lambda x, y: x*np.exp(1j*y), samples[h], phases[h]))
        samples[h] = ifft(samples[h])
        
        # overlap
        ind = int(f_size/2)
        
        for k in range(f_size):
            y[h*ind+k] = samples[h][k] + y[h*ind+k]
            
    return y

# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = "grabacion1.wav"
        
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

window_size = 400 #512
noise_frames = 100# máximo,como tenemos overlap 50%, 0,6s
alpha = 5
# tiempo
start = time.time()
y =spectralSubtraction(data, window_size, noise_frames, alpha)
print('tiempo filtrado del ruido: ', time.time() - start)
# write wav file
try:
    wavfile.write('/home/pi/wavfiles/ruidoless1.wav',
                       fs, y.real.astype(np.int16))
        #print('Escritura de archivo correcta') 
except IOError as e:
    #  # parent of IOError, OSError *and* WindowsError where available
    print('Error al escritura el archivo')
    print(e)
    
timel = np.arange(len(data))/fs
plt.plot(timel, data,'g--',timel, y.real, 'r--')#,time, data,'g--')

plt.title('spectral subtraction ')
plt.xlabel('Original green, resta red')
plt.show()

