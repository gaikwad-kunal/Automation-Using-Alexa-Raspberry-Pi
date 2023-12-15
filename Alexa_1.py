import speech_recognition as sr
import pyttsx3
import datetime
import random
import wikipedia
import pyjokes
import requests

from bs4 import BeautifulSoup
from wikipedia import exceptions
import os
import time
import sys
import speedtest
from PyDictionary import PyDictionary as Dict


listener = sr.Recognizer()
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
  
  speak("I am peter, Please tell me how can I help you ")


def takeCommand():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("I AM Listening...")
    r.pause_threshold = 1
    r.energy_threshold=4000
    audio = r.listen(source)

  try:
    print("Recognizing...")
    print("OK")
    query = r.recognize_google(audio, language='en-in')
    print(f"You said: {query}\n")


  except Exception as e:
    #speak("Say that again please...")  
    return "None"
  query=query.lower()
  return query

def TaskExecution():
  while True:
    query=takeCommand()
    

    if 'wikipedia' in query:
      speak('Searching Wikipedia...')
      query = query.replace("wikipedia", "")
      results = wikipedia.summary(query, sentences=1)
      speak("According to Wikipedia")
      print(results) 
      speak(results)
    
    elif 'the time' in query:
      strTime = datetime.datetime.now().strftime("%H:%M:%S")
      speak(f"the time is {strTime}")

    elif "date" in query:
      strTime=datetime.datetime.now().strftime("%d-%m-%y")
      speak(f"the today date is {strTime}")

    elif 'what can you do' in query:
      li_commands = {
      "joke": "Example: 'tell me a joke",
      "time": "Example: 'what time it is?'",
      "date": "Example: 'what date it is?'",
      "launch applications": "Example: 'activate fan or light'",
      "tell me": "Example: 'tell me who is President of India'",
      "weather": "Example: 'what weather/temperature in Kolhapur?'",
      "news": "Example: 'todays news' ",
      "Dictionary": "Example: 'what is Meaning/synonym/antonym of whatever word' "
      }
      ans = """I can do lots of things, for example you can ask me time, date, weather in your city,
        I can tell you any information about any subject, launch application and more. See the list of commands-"""
      speak(ans)
      speak(li_commands)
        
    elif 'how are you' in query:
      li = ['good', 'fine', 'great']
      response = random.choice(li)
      print(f"I am {response},what about you.")
      speak(f"I am {response},what about you.")

    elif "also good" in query or "fine" in query:
      print("That's great to hear from you.")
      speak("That's great to hear from you.")
      
    elif 'who are you' in query:
      print("I am Peter, I am your personal assistant")
      speak("I am Peter, I am your personal assistant")
    
    elif 'tell me a joke' in query:
      joke1=pyjokes.get_joke()
      print(joke1)
      speak(joke1)
    
    elif 'thank you' in query:
      speak("It's my pleasure.")

    elif 'temperature' in query:
      s="temperature in kolhapur"
      url=f"https://www.google.com/search?q={s}"
      r=requests.get(url)
      data=BeautifulSoup(r.text,"html.parser")
      temp=data.find("div",class_="BNeawe").text
      print(f"current {s} is {temp}")
      speak(f"current {s} is {temp}")
  
    elif "today's news" in query:
      News()
    
    elif 'where i am' in query or "where we are" in query:
      speak("wait,let me check")
      try:
        ipAdd=requests.get('https://api.ipify.org/').text
        print(ipAdd)
        url='https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
        geo_request=requests.get(url)
        geo_data=geo_request.json()
        city=geo_data['city']
        country=geo_data['country']
        state=geo_data["region"]
        speak(f"i am not sure,but i think we are in {city} city of {country}country")
      except exceptions as e:
        speak("Sorry, Due to network issue i am not able to find where we are.")
        pass
    
    elif 'hello' in query or 'hey' in query:
      speak("hello , may i help you something.")

    elif 'leave it' in query or 'leave now' in query:
      speak('ok')

    elif 'internet speed' in query:
      speak("Checking internet speed......")
      st=speedtest.Speedtest()
      dt=st.download()
      speak("geting information..., i will tell you shortly")
      downloadSpeed=int(dt/800000)
      up=st.upload()
      uploadingSpeed=int(up/800000)

      speak(f"we have {downloadSpeed} Megabits per second downloadspeed and {uploadingSpeed} Megabits per second uploading speed")
      print(f"we have {downloadSpeed} Megabits per second downloadspeed and {uploadingSpeed} Megabits per second uploading speed")

    elif 'tell me' in query:
      query=query.replace("tell me","")
      url=f"https://www.google.com/search?q={query}"
      r=requests.get(url)
      data=BeautifulSoup(r.text,"html.parser")
      temp=data.find("div",class_="BNeawe").text
      print(f"{temp}")
      speak(f"{temp}")

    elif 'dictionary' in query:
      dict()

    elif 'launch application' in query:
      application()

    elif 'you can sleep' in query or 'sleep now' in query:
      speak("okey, i am going to sleep you can call me anytime.")
      break
  
def dict():
  speak('dictionary opened')
  speak('tell me the question')
  question=takeCommand()
  if 'meaning' in question:
    question=question.replace("what is the","")
    question= question.replace("meaning","")
    question= question.replace("of","")
    result= Dict.meaning(question)
    print(result)
    speak(f"the meaning for {question}is {result}")

  elif 'synonym' in question:
    question=question.replace("what is the","")
    question= question.replace("synonym","")
    question= question.replace("of","")
    result= Dict.synonym(question)
    speak(f"the synonym for {question}is {result}")

  elif 'antonym' in question:
    question=question.replace("what is the","")
    question= question.replace("antonym","")
    question= question.replace("of","")
    result= Dict.antonym(question)
    speak(f"the antonym for {question}is {result}")

def News():
  speak('which news headline you want to listence')
  headline= takeCommand()
  if 'top five news in india' in headline:
    api_key="8b54bd15d633458f936ce3d796f391c3"
    url="https://newsapi.org/v2/top-headlines?country=in&apiKey="+api_key
    news=requests.get(url).json()
    article=news['articles']
    news_article=[]
    day=["first","second","third","fourth","fifth"]
    for arti in article:
      news_article.append(arti['title'])
    for i in range(5):
      print(i+1,news_article[i])
      speak(f"today's{day[i]} news is :{news_article[i]}")
  elif 'sport news' in headline:
      url='https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=8b54bd15d633458f936ce3d796f391c3'
      news=requests.get(url).json()
      article=news['articles']
      news_article=[]
      day=["first","second","third","fourth","fifth"]
      for arti in article:
        news_article.append(arti['title'])
      for i in range(5):
        print(i+1,news_article[i])
        speak(f"today's{day[i]} news is :{news_article[i]}")

def application():
  speak('lunching Home Automation System')
  speak('tell me which application you want to on or off')
  question=takeCommand()
  
  if 'tv' in question:
    url=" https://api.thingspeak.com/channels/1647882/fields/1/last.json"
    data=requests.get(url).json()
    status=data['field1']

    if status=="1":
      speak("Tv is on, can you make it off")
      ask=takeCommand()
      if 'yes' in ask:
        Status="0"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field1="+Status
        requests.get(url).json()
        speak("i am turning off the tv")
      elif 'no' in ask:
        Status="1"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field1="+Status
        requests.get(url).json()
        speak("ok")
    else:
      speak("Tv is off, can you make it on")
      ask=takeCommand()
      if 'yes' in ask:
        Status="1"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field1="+Status
        requests.get(url).json()
        speak("tv is activating...")
      elif 'no' in ask:
        Status="0"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field1="+Status
        requests.get(url).json()
        speak("ok")
 
  elif 'lamp' in question:
    url=" https://api.thingspeak.com/channels/1647882/fields/2/last.json"
    data=requests.get(url).json()
    status=data['field2']

    if status=="1":
      speak("lamp is on, can you make it off")
      ask=takeCommand()
      if 'yes' in ask:
        Status="0"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field2="+Status
        requests.get(url).json()
        speak("i am turning off the lamp")
      elif 'no' in ask:
        Status="1"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field2="+Status
        requests.get(url).json()
        speak("ok")
    else:
      speak("lamp is off, can you make it on")
      ask=takeCommand()
      if 'yes' in ask:
        Status="1"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field2="+Status
        requests.get(url).json()
        speak("lamp is activating...")
      elif 'no' in ask:
        Status="0"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field2="+Status
        requests.get(url).json()
        speak("ok")
 
  elif 'fan' in question:
    url=" https://api.thingspeak.com/channels/1647882/fields/3/last.json"
    data=requests.get(url).json()
    status=data['field3']

    if status=="1":
      speak("fan is on, can you make it off")
      ask=takeCommand()
      if 'yes' in ask:
        Status="0"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field3="+Status
        requests.get(url).json()
        speak("i am turning off the lamp")
      elif 'no' in ask:
        Status="1"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field3="+Status
        requests.get(url).json()
        speak("ok")
    else:
      speak("fan is off, can you make it on")
      ask=takeCommand()
      if 'yes' in ask:
        Status="1"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field3="+Status
        requests.get(url).json()
        speak("fan is activating...")
      elif 'no' in ask:
        Status="0"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field3="+Status
        requests.get(url).json()
        speak("ok")
  
  elif 'switch 4' in question:
    url=" https://api.thingspeak.com/channels/1647882/fields/4/last.json"
    data=requests.get(url).json()
    status=data['field4']

    if status=="1":
      speak("switch four is on, can you make it off")
      ask=takeCommand()
      if 'yes' in ask:
        Status="0"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field4="+Status
        requests.get(url).json()
        speak("i am turning off the switch four")
      elif 'no' in ask:
        Status="1"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field4="+Status
        requests.get(url).json()
        speak("ok")
    else:
      speak("switch four is off, can you make it on")
      ask=takeCommand()
      if 'yes' in ask:
        Status="1"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field4="+Status
        requests.get(url).json()
        speak("switch four is activating...")
      elif 'no' in ask:
        Status="0"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field4="+Status
        requests.get(url).json()
        speak("ok")
 
  elif 'curtains' in question:
    url=" https://api.thingspeak.com/channels/1647882/fields/4/last.json"
    data=requests.get(url).json()
    status=data['field5']

    if status=="1":
      speak("curtains is opened, can you make it close")
      ask=takeCommand()
      if 'yes' in ask:
        Status="0"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field5="+Status
        requests.get(url).json()
        speak("i am closing the curtains")
      elif 'no' in ask:
        Status="1"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field5="+Status
        requests.get(url).json()
        speak("ok")
    else:
      speak("curtains is closed, can you make it open")
      ask=takeCommand()
      if 'yes' in ask:
        Status="1"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field5="+Status
        requests.get(url).json()
        speak("i am opening the curtains")
      elif 'no' in ask:
        Status="0"
        url="https://api.thingspeak.com/update?api_key=4A8VE4Z6V6E68L4T&field5="+Status
        requests.get(url).json()
        speak("ok")



if __name__ == "__main__":
  while True:
    permission = takeCommand()
    if 'peter' in permission:
      li = ['yes', 'hey', 'hello']
      response = random.choice(li)
      speak(f"{response}, how may i help you.")
      TaskExecution()
    
    elif 'wake up' in permission:
      wishme()
      TaskExecution()

    elif 'goodbye' in permission:
      speak("thanks for using me sir, have a good day")
      sys.exit()