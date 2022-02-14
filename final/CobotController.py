import argparse
import os
import queue
import sys
import json
import sounddevice as sd
import vosk
import threading
import time
from Activities import Activities
from RaspiAPI import RaspiAPI
from InputChecker import InputChecker
import numpy as np

#Commands
STARTWORD = 'hallo computer'
Weiter_Command_Word = 'Weiter'
Start_Command_Word = 'Start'
Weiter_Command_Words = ['Weiter', 'weiter gehts', 'rausnehmen']
Start_Command_Words = ['Start', 'Los gehts', 'Beginne']
Abbruch_Command_Words = ['Abbruch', 'Halt', 'Stopp']

#Paths
Model_Path = '/home/pi/Sprachggesteuerte-Maschinenschnittstelle/final/model'

q = queue.Queue()
act =  None

class Speech: 
    
    STARTCODE = 'computer'
    def __init__(self,startcode):
        self.STARTCODE = startcode
    # Unsere Thread Funktion
    def thread_timer(self):
        Activities.Listen_Command(act,10)

    def isCommand(self, cmdWords, text):
        for word in cmdWords:
            #print(word.upper())
            #print(text)
            if word.upper() in text.upper():
                return True
        return False
        
    # Definieren der Aktivierungsphase. Solange der thread gestartet ist, können Kommandos zum triggern der Methoden aus der Activities Klasse gesagt werden.
    # 
    def active(self,rec):
        print("active")
        # Thread definieren
        t = threading.Thread(target=Speech.thread_timer)
        # Thread starten
        t.start()
        # solange Thread aktiv
        while t.is_alive():
            print('call a command')
            # hole die Daten aus der Queue, bzw. aus dem Stream
            data = q.get()
            if rec.AcceptWaveform(data):
                print("second record")
                res = json.loads(rec.Result())
                if self.checkCommands(res['text'].upper()):
                    break
                print(res['text'])

    def checkCommands(self, text):        
        #if Weiter_Command_Word.upper() in res['text'].upper():
        if self.isCommand(Weiter_Command_Words, text):
            Activities.weiter(act)
            return True
        elif self.isCommand(Start_Command_Words, text):
            Activities.start(act)
            return True
        elif self.isCommand(Abbruch_Command_Words, text):
            Activities.Abbruch(act)
            return True
        return False
        

    def Listen_Command(self,rec):
        print("start Listen")
        act.Ask_Weiter()
        t = threading.Thread(target=Speech.thread_timer)
        t.start()
        while t.is_alive():
            print("start to speak")
            data = q.get()            
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                text = res['text'].upper()
                print(rec.Result())
                if self.isCommand(Weiter_Command_Words, text):
                    Activities.weiter(act)
                    break
                elif self.isCommand(Abbruch_Command_Words, text):
                    Activities.Abbruch(act)
                    break
        print("fail")
        act.AskNext_NoInput()

    def listenWakeWord(self,rec):
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
                act.success_Sound()
                Speech.active(rec)
                act.fail_Sound()
            self.OneShot_Activation(Speech.STARTCODE, Weiter_Command_Words, res['text'])                   
        else:                
            pass

    def OneShot_Activation(self, StartCode, CommandArray, text):
            splitSymbol = " "
            splittedText = text.split(splitSymbol)
            splittedStartCode = StartCode.split(splitSymbol)
            x = 0
            while x < len(splittedStartCode):
                #print (splittedStartCode[x])
                #print (splittedText[0])
                if splittedStartCode[x] == splittedText[0]:
                    splittedText = np.delete(splittedText, 0)
                    #print (splittedText)
                    #print("Go on Oneshot")
                    x = x+1
                    pass
                else:
                     #print("Abbruch oneshot")
                    return
            #print(splitSymbol.join(splittedText))
            self.checkCommands(splitSymbol.join(splittedText))


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
        '-m','--model', type=str, nargs='?',default=Model_Path, help='Pfad zum Model'
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
        exit(1)
    model = vosk.Model(args.model)
    # Speech Objekt erstellen und Übergabe des Aktivierungsworts
    Speech = Speech(STARTWORD)    
    with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=None,dtype='int16',
                            channels=1, callback=callback):
        print('*' * 80)
        # Aktivierung der vosk Spracherkennung mit Übergabe des geladenen Models. Übersetze das Gesprochene in Text.
        rec = vosk.KaldiRecognizer(model, args.samplerate)
        api = RaspiAPI()
        act = Activities(api)
        ic = InputChecker(api)
        act.audio_Start()
        while True:
            # Daten aus der Queue ziehen
            is_speech_open = ic.Get_Speech_Open()
            is_EndSignal_active = ic.Get_End_Signal()
            is_AskNextSignal_active = ic.Get_AskNext_Signal()
            #print(f"{is_speech_open}")
            if is_EndSignal_active:
                print("End Command played")
                act.Play_End_Command_Sound()
            elif not is_speech_open:
                #Queue leeren
                data = q.get() 
                act.Speech_Recognition_Closed()
            elif is_AskNextSignal_active:
                Speech.Listen_Command(rec)
            else:
                Speech.listenWakeWord(rec)
                