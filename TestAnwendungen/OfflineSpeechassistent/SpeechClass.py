import argparse
import os
import queue
import sys
import json
import sounddevice as sd
import vosk
import threading
import time
import gpiozero
import RPi.GPIO as GPIO
import simpleaudio as sa

q = queue.Queue()

class Activities:
# Definiere die Aktivitäten, die mit deiner Sprache gesteuert werden können.
    LICHT_LED = LED_TOR = None
    
    def licht(GPIO):
        # Schalte das Licht an und aus
        print(f" Schalte das Licht an/aus mit {GPIO}")
        if Activities.LICHT_LED is None:
            Activities.LICHT_LED = gpiozero.LED(GPIO)
        try:
            Activities.LICHT_LED.toggle()
            
        # if any error occurs call exception
        except gpiozero.GPIOZeroError as err:
            print("Error occured: {0}".format(err))
    
    def tor(GPIO):
        # zur Demonstrationszwecken wird hier nun eine Ausgabe definiert. 
        print(f" Schalte das Tor an mit {GPIO}")

    





class speech: 
    
    STARTCODE = 'computer'
    def __init__(self,startcode):
        self.STARTCODE = startcode
    # Unsere Thread Funktion
    def thread_timer(self):
        # Aktiviere GPIO 17, um die grüne LED zum Leuchten zu bringen. 
        led = gpiozero.LED(17)
        self.power_gpio(17,led)
        # warte 10 Sekunden
        time.sleep(10)
        # Schalte die grüne LED wieder aus.
        self.close_gpio(17,led)

    def gpio_Input(self):
        #Statusausgabe bei Eingangssignal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.IN)
        filename = 'TestSounds/Ok.wav'
        wave_object = sa.WaveObject.from_wave_file(filename)
        while True:
            if GPIO.input(19) == 0:
                pass
            else:
                play_obj = wave_object.play()
                play_obj.wait_done() 
        
    # Definieren der Aktivierungsphase. Solange der thread gestartet ist, können Kommandos zum triggern der Methoden aus der Activities Klasse gesagt werden.
    # 
    def active(self,rec):
        print("active")
        # Thread definieren
        t = threading.Thread(target=self.thread_timer)
        # Thread starten
        t.start()
        i=0
        # solange Thread aktiv
        while t.is_alive():
            print('call a command')
            # hole die Daten aus der Queue, bzw. aus dem Stream
            data = q.get()
            if rec.AcceptWaveform(data):
                print("second record")
                # 
                res = json.loads(rec.Result())
                if 'LICHT'.upper() in res['text'].upper():
                    Activities.licht(18)
                elif 'Tor'.upper() in res['text'].upper():
                    Activities.tor(18)
                print(res['text'])
    def power_gpio(self,GPIO,led):
        print(f"Power {GPIO}")
        try:
            # switch LED on
            if not led.is_lit:
                led.on()
        # if any error occurs call exception
        except gpiozero.GPIOZeroError as err:
            print("Error occured: {0}".format(err))
    
    def close_gpio(self,GPIO,led):
        print(f"Close {GPIO}")
        try:
            # switch LED off
            if led.is_lit:
                led.off()
        # if any error occurs call exception
        except gpiozero.GPIOZeroError as err:
            print("Error occured: {0}".format(err))

#Main Klasse
def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
        pass
    q.put(bytes(indata))
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        '-m','--model', type=str, nargs='?',default='/home/pi/Sprachggesteuerte-Maschinenschnittstelle/TestAnwendungen/vosk-api/python/example/model', help='Pfad zum Model'
        #'-m','--model', type=str, nargs='?',default='../vosk-api/python/BigModel/model', help='Pfad zum größeren Model'
        #'-m','--model', type=str, nargs='?',default='model', help='Pfad zum größeren Model'
    )
    parser.add_argument(
        '-d','--device', type=str,nargs='?',default='1,0',help='Eingabegerät(Mikrofon als String)'
    )
    parser.add_argument(
        '-r','--samplerate',type=int,nargs='?', default=44100,help='Sample Rate'
    )
    args = parser.parse_args('')
    if not os.path.exists(args.model):
        print("Please download a model from https://alphacephei.com/vosk/models and unpack to 'model'")
        #exit(1)
    model = vosk.Model(args.model)
    # Speech Objekt erstellen und Übergabe des Aktivierungsworts
    speech = speech('computer')
    # 
    with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=None,dtype='int16',
                            channels=1, callback=callback):
        print('*' * 80)
        # Aktivierung der vosk Spracherkennung mit Übergabe des geladenen Models. Übersetze das Gesprochene in Text.
        rec = vosk.KaldiRecognizer(model, args.samplerate)
        t = threading.Thread(target=speech.gpio_Input)
        # Thread starten
        t.start()
        while True:
            # Daten aus der Queue ziehen
            data = q.get()
            print("start to speak")
            if rec.AcceptWaveform(data):
                # erhalte das erkannte gesprochene als String zurück
                x = rec.Result()
                print(x)
                print(rec.Result())
                # wandelt den String in Json um
                res = json.loads(x)
                print(res)
                # wenn der Aktivierungscode herausgehört wurde, wird die active Methode von Speech gestartet
                if speech.STARTCODE == res['text']:
                    speech.active(rec)
            else:
                pass