# compresor expansor tiempo real 
import numpy as np
import pyaudio
import time

# dispositivo de entrada / salida
dev_index = 2 # device index found by p.get_device_info
RATE = 44100

th_comp= -5 # dB
th_exp = -75 # dB
th_comp16 = 10**(th_comp /20)* 32769 # 2¹⁵
th_exp16 = 10**(th_exp /20)* 32769
CR  = 4

def comprexpander(x, ratio, th_c, th_e):
    # x Señal de entrada
    # ratio ratio de compresión / expansión
    # th_c umbrar compreción
    # th_e umbral expansión
    
    #th_c = 10**(th_c /20)* 32769 # 2¹⁵
    #th_e = 10**(th_e /20)* 32769 # esta operación debe estar fuera
    cn = np.zeros(1024)# salida detector de nivel
    gain = np.ones(1024)
    #gain_c = np.ones(len(x))
    #gain_e = np.ones(len(x))
    out = np.zeros(1024)
    out[0] = x[0]
    cn[0] = abs(x[0])
    for i in range(1,1024):
        cn[i] = abs(x[i])
        if abs(x[i]) > th_c :
            # compresión
            if cn[i] > cn[i-1]:
                cn[i] = cn[i]
            else:
                cn[i] = cn[i-1]
            # ganancia   
            gain[i] = (cn[i] / th_c)**(1/ratio - 1)
        elif abs(x[i]) < th_e :
            if abs(x[i]) > 10:
                # expansión si no es ruido
                gain[i] =1/ (cn[i] /th_e)**(ratio -1)
            else:
                # ruido
                gain[i] = 0
        else:
            gain[i] = 1
        out[i] = gain[i] * x[i]
        
    return out

pa= pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    # tiempo
    c = np.random.randint(100)
    if c == 30:
        s = time.time()
    # convert data to array
    data = np.frombuffer(in_data, np.int16)
    #data1 = data.copy()
    # hacemos el computo
    #data1 = data1/ norm # valores entre 1 y -1
    #datan = data / 32768  # 2¹⁶ /2
    #y = comprexpander(data, CR, th_comp, th_exp)
    y = comprexpander(data, CR, th_comp16, th_exp16)

    #y = y * 32768

    
    sample = y.astype(np.int16).tostring()
    #return (in_data, pyaudio.paContinue)
    if c == 30:
        print('tiempo compresor: ', time.time() - s)
    return (sample, pyaudio.paContinue)
# open stream
stream = pa.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        #input = True,
        #output = True,
        input_device_index = dev_index,input = True,
        output_device_index = dev_index,output = True,
        stream_callback = callback)

stream.start_stream()

while stream.is_active():
    print("Stream is active")
    time.sleep(10)
    stream.stop_stream()
    print("Stream is stopped")

stream.stop_stream()
stream.close()

pa.terminate()
