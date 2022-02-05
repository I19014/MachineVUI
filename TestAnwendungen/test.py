import pyttsx3


engine = pyttsx3.init()


engine.setProperty('voice', 'german')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-100)
volume = engine.getProperty('volume')
engine.setProperty('volume', volume+1.25)
engine.say("Ich Liebe dich")
engine.runAndWait()