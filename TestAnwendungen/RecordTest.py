import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

fs = 44400
duration = 3.5

recording = sd.rec(int(duration*fs),samplerate = fs, channels = 2)
sd.wait()
write("TestSounds/recording.wav",fs,recording)
wv.write("TestSounds/recording1.wav", recording, fs, sampwidth=2)