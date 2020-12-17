import sys
import os
import pyaudio
import wave

# entrada de argumentos
try:
    if len(sys.argv) == 1:
        file_input = 'grabacion1.wav'
    else:
        file_input = sys.argv[1]
        print(sys.argv[1])
except IOError as ex:
    print(ex)
    

chunk = 4096 # 2^12 samples for buffer
sample_format = pyaudio.paInt16 # 16 bits per sample
channels = 1
fs = 44100 # record at 44100 samples per second
seconds = 10
filename = '/home/pi/wavfiles/'+file_input
#filename = file_input

p = pyaudio.PyAudio() # Create an interface to PortAudio

print('Recording')

stream = p.open(format = sample_format,
                channels = channels,
                rate = fs,
                input = True,
                frames_per_buffer = chunk)

frames = [] # Initialize array to store frames

# Store data in chunks for 10 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

print('Finished recording')
# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio Interface
p.terminate()

# Save the recorded data as a wav file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

# plays the audio file
os.system("aplay /home/pi/wavfiles/grabacion1.wav")
                
