# Imports
import speech_recognition as sr
from googletrans import Translator
from googletrans import Translator
import subprocess
import pyjokes
import requests
from langdetect import detect
from googletrans import Translator
import pywhatkit as kit
import psutil
import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to recognize speech
def recognize_speech():
  recognizer = sr.Recognizer()
  with sr.Microphone() as source:
    print("Speak your sentence:")
    audio = recognizer.listen(source)
  try:
    text = recognizer.recognize_google(audio)
    print("You said: " + text)
    return text
  except sr.UnknownValueError:
    print("Could not understand audio")
    return None
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None
  
def translate_text(text, source_lang, target_lang):
  translator = Translator()
  translation = translator.translate(text, src=source_lang, dest=target_lang)
  return translation.text




def execute_intent(intent, language):
    if language == 'en':
        if "open google" in intent:
            subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])
            return "Opening Google Chrome..."
        elif "show me images" in intent:
            return "Showing images..."
        elif "how are you" in intent:
            return "I'm fine, thank you!"
        elif "tell me a joke" in intent:
            return pyjokes.get_joke()
        elif "news" in intent:
            news = get_news()
            return f"Here are the latest news headlines: {news}"
        elif "play" in intent:
            search_query = intent.replace("play", "")
            kit.playonyt(search_query)
            return f"Playing {search_query} on YouTube..."
        elif "email" in intent:
            return "Please provide email details."
        elif "covid tracker" in intent:
            return "Fetching COVID tracker information..."
        elif "weather" in intent:
            return "Please provide city name for weather information."
        elif "battery" in intent:
            battery_percent = psutil.sensors_battery().percent
            return f"My battery is at {battery_percent}%"
        elif "time" in intent:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
        elif "volume" in intent:
            return "Controlling volume..."
        elif "search" in intent:
            return "Performing web search..."
        elif "shutdown" in intent:
            os.system("shutdown /s /t 1")
            return "Shutting down system..."
        else:
            return "Sorry, I'm not sure what you're asking for."
    else:
        return "Sorry, I currently only understand commands in English."
    
def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'country': 'in', 
            'apiKey': '2cbaf2d8bc7f4c9a8a3db5c29a63b28c'  
        }
        response = requests.get(url, params=params)
        news_data = response.json()
        headlines = [article['title'] for article in news_data['articles']]
        return "\n".join(headlines[:5])
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "Sorry, unable to fetch news at the moment."

def get_weather(city):
    api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"The weather in {city} is {weather_desc} with a temperature of {temp}°C"
        else:
            return "Sorry, unable to fetch weather information."
    except Exception as e:
        print(f"Error fetching weather information: {e}")
        return "Sorry, unable to fetch weather information."

def send_email(sender_email, sender_password, receiver_email, subject, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server.send_message(msg)
        server.quit()

        return "Email sent successfully."
    except Exception as e:
        print(f"Error sending email: {e}")
        return "Sorry, unable to send email."

# Main program
text = recognize_speech()
if text:
  translated_text = translate_text(text, 'auto', 'en') 
  execute_intent(translated_text.lower(),'en')
  print("Translated Text:", translated_text.lower())
