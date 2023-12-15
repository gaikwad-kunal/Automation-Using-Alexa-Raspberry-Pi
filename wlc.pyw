import pyttsx3
import datetime
import time


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate',170)

def speak(audio):
  engine.say(audio)
  engine.runAndWait()

def wishme():
  hour=int(datetime.datetime.now().hour)
  t=time.strftime("%I:%M %p")
  if hour>=0 and hour<12:
    speak(f"Good Morning! , its {t}")

  elif hour>=12 and hour<18:
    speak(f"Good Afternoon!, its {t}")

  else:
    speak(f"good Evening! , its {t}")
  
  speak("I am Lapi, I AM READY TO LUNCH ")

wishme()
