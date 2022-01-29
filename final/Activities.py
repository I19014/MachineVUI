import gpiozero
#from Speech import Speech

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
    
    def impuls(GPIO):
        #Pin ist für 2 Sekunden auf High
        led = gpiozero.LED(GPIO)
        #speech.power_gpio(GPIO,led)
        # warte 10 Sekunden
        time.sleep(2)
        # Schalte die grüne LED wieder aus.
        #speech.close_gpio(GPIO,led)