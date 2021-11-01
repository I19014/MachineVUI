import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import RPi.GPIO as io
import wavio as wv

fs = 44400
duration = 3.5
filename = "TestSounds/TempAudio.wav"
r = sr.Recognizer()
#Init LED
led1 = 22
io.setmode(io.BCM)
io.setup(led1, io.OUT)

print("Reden!")
recording = sd.rec(int(duration*fs),samplerate = fs, channels = 2)
sd.wait()
wv.write(filename, recording, fs, sampwidth=2)

with sr.AudioFile(filename) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)

if text == "on":
    io.output(led1, True)
elif text == "off":
    io.output(led1, False)
