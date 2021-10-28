import RPi.GPIO as io
import time

led1 = 22

io.setmode(io.BCM)

io.setup(led1, io.OUT)

io.output(led1, True)
time.sleep(5)
io.output(led1, False)