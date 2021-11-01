import simpleaudio as sa
import RPi.GPIO as io
import time

filename = 'TestSounds/test.wav'
led1 = 22

io.setmode(io.BCM)
io.setup(led1, io.OUT)


wave_object = sa.WaveObject.from_wave_file(filename)
io.output(led1, True)
play_obj = wave_object.play()
play_obj.wait_done() 
io.output(led1, False)