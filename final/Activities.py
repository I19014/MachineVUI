import gpiozero
from RaspiAPI import RaspiAPI
import threading

class Activities:
# Definiere die Aktivitäten, die mit deiner Sprache gesteuert werden können.
    LICHT_LED = LED_TOR = None
    RaspiAPI = RaspiAPI()      
    
    def __init__(self):
        self.init_Command_End_Signal()
        print("init Activities")

    # Console Output
    def pin_Info(self,text,GPIO):
        # zur Demonstrationszwecken wird hier nun eine Ausgabe definiert. 
        print(f"Action: {text}: {GPIO}")

    # Voice Commands

    def speakSignal(self, time):
        GPIO = 25
        RaspiAPI.power_gpio_time(RaspiAPI,GPIO,time)
        self.pin_Info("Open for Commands; Open Pin for 10 sec", GPIO)

    def start(self):
        pin = 18
        Activities.success_Sound()
        Activities.impuls(pin)
        self.pin_Info("Run Command 'Start'; Impulse Pin", pin)
    
    def weiter(self):
        pin = 23
        Activities.success_Sound()
        Activities.impuls(pin)
        self.pin_Info("Run Command 'Weiter'; Impulse Pin", pin)
    
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
        filename = 'audio/SystemStart.wav'
        RaspiAPI.play_Audio(filename)
        print("Play start audio")

    def success_Sound():
        filename = 'audio/Success.wav'
        RaspiAPI.play_Audio(filename)
        print("Play success audio")

    def fail_Sound():
        filename = 'audio/Fail.wav'
        RaspiAPI.play_Audio(filename)
        print("Play fail audio")

    #Machine Signals
    def init_Command_End_Signal(self):
        t = threading.Thread(target=self.Command_End_Signal)
        t.start()
        print("Start Thread")

    def Command_End_Signal(self):
         filename = 'audio/Success.wav'
         pin = 17
         RaspiAPI.gpio_Input(RaspiAPI,pin, filename)