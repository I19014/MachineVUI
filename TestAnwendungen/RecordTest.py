import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

fre = 44400
duration = 3.5

recording = sd.rec(int(duration*fre),samplerate = freq, channels = 2)
sd.wait()
write("recording.wav",freq,recording)
wv.write("recording1.wav", recording, freq, sampwidth=2)