import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import simpleaudio as sa
import numpy as np

fs = 44100
duration = 3.5
filename = 'TestSounds/Ok.wav'

#Record Voice
recording = sd.rec(int(duration*fs),samplerate = fs, channels = 2)
print('Start Recording')
sd.wait()
print('Finished Recording')
wv.write(filename, recording, fs, sampwidth=2)

#play recorded File
wave_object = sa.WaveObject.from_wave_file(filename)
play_obj = wave_object.play()
print('Play')
play_obj.wait_done() 
print('done')