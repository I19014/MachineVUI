import gpiozero
from RaspiAPI import RaspiAPI
import threading

#Audio Files
Success_Audio = 'audio/Success.wav'
Fail_Audio = 'audio/Fail.wav'
Start_Audio = 'audio/SystemStart.wav'

# Output Pins
Listen_Command_Pin = 25
Weiter_Pin = 18
Start_Pin = 23

#Input Pins
Command_finished_Pin = 17

class Activities:
# Definiere die Aktivitäten, die mit deiner Sprache gesteuert werden können.
    LICHT_LED = LED_TOR = None
    RaspiAPI = RaspiAPI()      
    
    def __init__(self):
        self.init_Command_End_Signal()

    # Console Output
    def pin_Info(self,text,GPIO):
        # zur Demonstrationszwecken wird hier nun eine Ausgabe definiert. 
        print(f"Action: {text}: {GPIO}")

    # Voice Commands

    def Listen_Command(self, time):
        RaspiAPI.power_gpio_time(RaspiAPI,Listen_Command_Pin,time)
        self.pin_Info("Open for Commands; Open Pin for 10 sec", Listen_Command_Pin)

    def start(self):
        Activities.success_Sound()
        Activities.impuls(Start_Pin)
        self.pin_Info("Run Command 'Start'; Impulse Pin", Start_Pin)
    
    def weiter(self):
        Activities.success_Sound()
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

    def audio_Start():
        RaspiAPI.play_Audio(Start_Audio)
        print("Play start audio")

    def success_Sound():
        RaspiAPI.play_Audio(Success_Audio)
        print("Play success audio")

    def fail_Sound():
        RaspiAPI.play_Audio(Fail_Audio)
        print("Play fail audio")

    #Machine Signals
    def init_Command_End_Signal(self):
        t = threading.Thread(target=self.Command_Finished_Signal)
        t.start()

    def Command_Finished_Signal(self):
         RaspiAPI.gpio_Input(RaspiAPI,Command_finished_Pin, Success_Audio)