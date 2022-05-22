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
from Word import Word as custom_Word
import numpy as np

#Commands
STARTWORD = 'hallo anlage'
STARTWORD2 = 'hallo computer'
Weiter_Command_Word = 'Weiter'
Start_Command_Word = 'Start'
Weiter_Command_Words = ['Weiter', 'weiter gehts', 'rausnehmen', 'entnehmen']
Start_Command_Words = ['Start', 'Los geht''s', 'Beginne', 'Vorrichtung einlegen', 'einlegen']
Abbruch_Command_Words = ['Abbruch', 'Halt', 'Stopp', 'Nein', "Nein danke", 'Bitte nicht', 'abbrechen']
Verabschiedung_Command_Words = ['tschau', 'tschüss', 'Auf Wiedersehen', 'Bis Bald', 'Machs gut', 'Ade', 'Auf Wiederhören']
Begrüßung_Command_Words = ['Wie gehts', "was geht", 'Was machen wir heute', 'hilfe', 'helfe', 'helfen']
bestätigende_Antwort_Command_Words = ['Ja', 'bitte', 'Ja bitte', 'gerne', 'gerne doch']

#Paths
Model_Path = '/home/pi/Sprachggesteuerte-Maschinenschnittstelle/final/model'

q = queue.Queue()
act =  None

class Speech: 
    
    STARTCODE = STARTWORD
    STARTCODE2 = STARTWORD2
    def __init__(self,startcode):
        self.STARTCODE = startcode
    # Unsere Thread Funktion
    def thread_timer(self):
        Activities.Listen_Command(act,10)

    def isCommand(self, cmdWords, text):
        for word in cmdWords:
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
        elif self.isCommand(Begrüßung_Command_Words, text):
            Activities.hallo_Command(act)
            return True
        elif self.isCommand(Verabschiedung_Command_Words, text):
            Activities.goodbye_Command(act)
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
                if self.isCommand(bestätigende_Antwort_Command_Words, text):
                    Activities.weiter(act)
                    break
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
        results = []
        if rec.AcceptWaveform(data):
            # erhalte das erkannte gesprochene als String zurück
            x = rec.Result()
            print("accepted")
            #print(x)
            #print(rec.Result())
            # wandelt den String in Json um
            res = json.loads(x)
            text = res['text']
            if text == "":
                return
            print('Understanded Text: ' + text)
            results.append(x)
            list_of_Words = []      
            for obj in res['result']:
                w = custom_Word(obj)  # create custom Word object
                list_of_Words.append(w)  # and add it to list  # and add it to list
            for word in list_of_Words:
                print(word.to_string())
            # wenn der Aktivierungscode herausgehört wurde, wird die active Methode von Speech gestartet
            self.OneShot_Activation(Speech.STARTCODE, Weiter_Command_Words, res['text'])
            if Speech.STARTCODE in text or Speech.STARTCODE2 in text or 'hallo' in text or 'anlage' in text or 'computer' in text:
                act.success_Sound()
                Speech.active(rec)
                act.fail_Sound()
            
            
            
                               
        else:                
            pass

    def OneShot_Activation(self, StartCode, CommandArray, text):
            splitSymbol = " "
            splittedText = text.split(splitSymbol)
            splittedStartCode = StartCode.split(splitSymbol)
            x = 0
            if text.startswith(StartCode):
                self.checkCommands(text)
            
            #print(splitSymbol.join(splittedText))
            


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
        rec.SetWords(True)
        api = RaspiAPI()
        act = Activities(api)
        ic = InputChecker(api)
        act.tts_start()
        while True:
            # Daten aus der Queue ziehen
            is_speech_open = ic.Get_Speech_Open()
            is_EndSignal_active = ic.Get_End_Signal()
            is_AskNextSignal_active = ic.Get_AskNext_Signal()
            #print(f"{is_speech_open}")
            #if is_EndSignal_active:
                #print("End Command played")
                #act.Play_End_Command_Sound()
            if not is_speech_open:
                #Queue leeren
                data = q.get() 
                act.Speech_Recognition_Closed()
            elif is_AskNextSignal_active:
                Speech.Listen_Command(rec)
            else:
                Speech.listenWakeWord(rec)
                