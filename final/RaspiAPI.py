import gpiozero
import RPi.GPIO as GPIO
import simpleaudio as sa
import time


class RaspiAPI:
    def gpio_Input(self, pin, filename):
        #Statusausgabe bei Eingangssignal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        while True:
            #print(f"Pin: {pin} Input: {GPIO.input(pin)}")
            if GPIO.input(pin) == 1:
                self.play_Audio(filename)
            time.sleep(0.5)
    

    def play_Audio(audio):
        filename = audio
        wave_object = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_object.play()
        play_obj.wait_done()

    def power_gpio(GPIO,led):
        print(f"Power {GPIO}")
        try:
            # switch LED on
            if not led.is_lit:
                led.on()
        # if any error occurs call exception
        except gpiozero.GPIOZeroError as err:
            print("Error occured: {0}".format(err))
    
    def close_gpio(GPIO,led):
        print(f"Close {GPIO}")
        try:
            # switch LED off
            if led.is_lit:
                led.off()
        # if any error occurs call exception
        except gpiozero.GPIOZeroError as err:
            print("Error occured: {0}".format(err))


    def power_gpio_time(self,GPIO,sleepTime):
        led = gpiozero.LED(GPIO)
        self.power_gpio(GPIO,led)
        # warte 10 Sekunden
        time.sleep(sleepTime)
        # Schalte die grüne LED wieder aus.
        self.close_gpio(GPIO,led)