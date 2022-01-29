import gpiozero
from RaspiAPI import RaspiAPI

class Activities:
# Definiere die Aktivitäten, die mit deiner Sprache gesteuert werden können.
    LICHT_LED = LED_TOR = None
    RaspiAPI = RaspiAPI()

    def speakSignal(GPIO, time):
        RaspiAPI.power_gpio_time(RaspiAPI,GPIO,time)

    
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
    
    def impuls(GPIO):
        RaspiAPI.power_gpio_time(RaspiAPI,GPIO,2)
    
    def audio_Start():
        filename = 'audio/SystemStart.wav'
        RaspiAPI.play_Audio(filename)

    def success_Sound():
        filename = 'audio/Success.wav'
        RaspiAPI.play_Audio(filename)

    def fail_Sound():
        filename = 'audio/Fail.wav'
        RaspiAPI.play_Audio(filename)