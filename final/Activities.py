import gpiozero
from RaspiAPI import RaspiAPI
import threading

#Audio Files
Directory = '/home/pi/Sprachggesteuerte-Maschinenschnittstelle/final/audio'
Success_Audio = 'Success.wav'
Fail_Audio = 'Fail.wav'
Start_Audio = 'SystemStart.wav'

# Output Pins
Listen_Command_Pin = 25
Weiter_Pin = 18
Start_Pin = 23

#Input Pins
Command_finished_Pin = 17
Speech_open_Pin = 4

class Activities:
# Definiere die Aktivitäten, die mit deiner Sprache gesteuert werden können.
    LICHT_LED = LED_TOR = None
    RaspiAPI = None      
    
    def __init__(self, raspi):
        RaspiAPI = raspi
        #self.init_Command_End_Signal()
        #self.Init_Speech_open()
        #for thread in threading.enumerate(): 
            #Wprint(thread.name)

    # Console Output
    def pin_Info(self,text,GPIO):
        # zur Demonstrationszwecken wird hier nun eine Ausgabe definiert. 
        print(f"Action: {text}: {GPIO}")

    # Voice Commands

    def Listen_Command(self, time):
        RaspiAPI.power_gpio_time(RaspiAPI,Listen_Command_Pin,time)
        self.pin_Info("Open for Commands; Open Pin for 10 sec", Listen_Command_Pin)

    def start(self):
        self.success_Sound()
        Activities.impuls(Start_Pin)
        self.pin_Info("Run Command 'Start'; Impulse Pin", Start_Pin)
    
    def weiter(self):
        self.success_Sound()
        Activities.impuls(Weiter_Pin)
        self.pin_Info("Run Command 'Weiter'; Impulse Pin", Weiter_Pin)
    
    # print Pins

    def impuls(GPIO):
        RaspiAPI.power_gpio_time(RaspiAPI,GPIO,2)

    def toggle_Output(GPIO):
        # Schalte das Licht an und aus
        print(f" Schalte das Licht an/aus mit {GPIO}")
        if Activities.LICHT_LED is None:
            Activities.LICHT_LED = gpiozero.LED(GPIO)
        try:
            Activities.LICHT_LED.toggle()
            
        # if any error occurs call exception
        except gpiozero.GPIOZeroError as err:
            print("Error occured: {0}".format(err))
    
    # print Audio

    def Play_End_Command_Sound(self):
        self.success_Sound()
        RaspiAPI.reset_End_Signal(RaspiAPI)

    def audio_Start(self):
        filename =self.buildPath(Start_Audio)
        RaspiAPI.play_Audio(filename)
        print("Play start audio")

    def success_Sound(self):
        filename =self.buildPath(Success_Audio)
        RaspiAPI.play_Audio(filename)
        print("Play success audio")

    def fail_Sound(self):
        filename =self.buildPath(Fail_Audio)
        RaspiAPI.play_Audio(filename)
        print("Play fail audio")

    #Machine Signals
    def init_Command_End_Signal(self):
        t = threading.Thread(target=self.Command_Finished_Signal)
        t.name = 'Command_End_Thread'
        t.start()

    def Command_Finished_Signal(self):
        filename = self.buildPath(Success_Audio) 
        RaspiAPI.gpio_Input(RaspiAPI,Command_finished_Pin, filename)

    def Init_Speech_open(self):
        t = threading.Thread(target=self.Speech_open)
        t.name = 'Speech_Open_Thread'
        t.start()

    def Speech_open(self):
        RaspiAPI.Speech_Open_Input(RaspiAPI, Speech_open_Pin)

    #Helper functions
    def buildPath(self, audio_File):
         return f"{Directory}/{audio_File}"

    def Is_Speech_Open(self):
        return RaspiAPI.IsSpeechOpen