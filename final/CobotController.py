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
from Speech import Speech
from Activities import Activities

q = queue.Queue()

class Speech: 
    
    STARTCODE = 'computer'
    def __init__(self,startcode):
        self.STARTCODE = startcode
    # Unsere Thread Funktion
    def thread_timer(self):
        Activities.speakSignal(17,10)
        
    # Definieren der Aktivierungsphase. Solange der thread gestartet ist, können Kommandos zum triggern der Methoden aus der Activities Klasse gesagt werden.
    # 
    def active(self,rec):
        print("active")
        # Thread definieren
        t = threading.Thread(target=Speech.thread_timer)
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
                if 'Weiter'.upper() in res['text'].upper():
                    Activities.success_Sound()
                    Activities.impuls(18)
                    #t.Join()
                    break
                elif 'Start'.upper() in res['text'].upper():
                    Activities.success_Sound()
                    Activities.impuls(23)
                    #t.Join()
                    break
                print(res['text'])

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
        '-m','--model', type=str, nargs='?',default='/home/pi/Sprachggesteuerte-Maschinenschnittstelle/TestAnwendungen/OfflineSpeechassistent/model', help='Pfad zum Model'
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
    Speech = Speech('hallo computer')    
    # 
    with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=None,dtype='int16',
                            channels=1, callback=callback):
        print('*' * 80)
        # Aktivierung der vosk Spracherkennung mit Übergabe des geladenen Models. Übersetze das Gesprochene in Text.
        rec = vosk.KaldiRecognizer(model, args.samplerate)
        #t = threading.Thread(target=Speech.gpio_Input)
        # Thread starten
        #t.start()
        Activities.audio_Start()
        while True:
            # Daten aus der Queue ziehen
            data = q.get()
            print("start to speak")
            if rec.AcceptWaveform(data):
                # erhalte das erkannte gesprochene als String zurück
                x = rec.Result()
                print("accepted")
                print(x)
                print(rec.Result())
                # wandelt den String in Json um
                res = json.loads(x)
                print(res)
                # wenn der Aktivierungscode herausgehört wurde, wird die active Methode von Speech gestartet
                if Speech.STARTCODE == res['text']:
                    Activities.success_Sound()
                    Speech.active(rec)
                    Activities.fail_Sound()                    
            else:                
                pass