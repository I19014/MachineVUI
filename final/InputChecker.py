import threading
from RaspiAPI import RaspiAPI

#Input Pins
Command_finished_Pin = 17
Speech_open_Pin = 23
Ask_Next_Pin = 25

class InputChecker:

    RaspiAPI = None

    def __init__(self, raspi):
        RaspiAPI = raspi
        #self.init_Command_End_Signal()
        self.Init_Speech_open()
        self.Init_ask_Next()
    
    #Init of Checkers
    def init_Command_End_Signal(self):
        t = threading.Thread(target=self.Command_Finished_Signal)
        t.name = 'Command_End_Thread'
        t.start()

    def Init_Speech_open(self):
        t = threading.Thread(target=self.Speech_open)
        t.name = 'Speech_Open_Thread'
        t.start()

    def Init_ask_Next(self):
        t = threading.Thread(target=self.Ask_Next)
        t.name = 'Ask_Next_Thread'
        t.start()

    #Checkers
    def Command_Finished_Signal(self):
        #filename = self.buildPath(Success_Audio) 
        RaspiAPI.End_Signal_Input(RaspiAPI,Command_finished_Pin)

    def Speech_open(self):
        RaspiAPI.Speech_Open_Input(RaspiAPI, Speech_open_Pin)

    def Ask_Next(self):
        RaspiAPI.Ask_Next_Input(RaspiAPI, Ask_Next_Pin)

    #Getter
    def Get_Speech_Open(self):
        return RaspiAPI.IsSpeechOpen

    def Get_End_Signal(self):
        return RaspiAPI.GotEndSignal

    def Get_AskNext_Signal(self):
        return RaspiAPI.AskGoNext