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
import re
# import googlemaps
import google.generativeai as genai
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


def calculate_expression(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        print(f"Error calculating expression: {e}")
        return None

def execute_intent(intent, language):
    if language == 'en':
        if any(keyword in intent for keyword in ['code', 'what', 'how to', 'show me', 'where', 'who']):
            if('time' in intent):
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                return f"The current time is {current_time}"
            elif('weather' in intent):
                return get_weather(intent)
            else:
                return ask_code(intent)
        elif "how are you" in intent:
            return "I'm fine, thank you!"
        elif "tell me a joke" in intent:
            return pyjokes.get_joke()
        elif "news" in intent:
            news = get_news()
            return f"Here are the latest news headlines: {news}"
        elif "how much is" in intent:  
            match = re.search(r'how much is\s*(.*)', intent)
            if match:
                expression = match.group(1)
                expression = expression.replace("x", "*").replace("÷", "/").replace("-", "-")
                result = calculate_expression(expression)
                if result is not None:
                    return f"The result of {expression} is {result}."
                else:
                    return "Sorry, I couldn't calculate the expression."
            else:
                return "Sorry, I couldn't understand the expression."
        elif "play" in intent and "YouTube" in intent.lower():
            search_query = intent.replace("play", "").replace("YouTube", "")
            kit.playonyt(search_query)
            return f"Playing {search_query} on YouTube..."
        elif "play" in intent:
            search_query = intent.replace("play", "")
            kit.playonyt(search_query)
            return f"Playing {search_query} on YouTube..."
        elif "weather" in intent:
            return get_weather('bangalore')
        elif 'battery' in intent:
            battery_percent = psutil.sensors_battery().percent
            return f"My battery is at {battery_percent}%"
        elif "time" in intent:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
        elif "search" in intent:
            return ask_code(intent)
        else:
            return ask_code(intent)
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
    api_key = '7ad5906cf9f5e459dc5adcced89db371'
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
    
def get_live_match_scores():
    try:
        url = "https://api.cricapi.com/v1/series_info?apikey=59383ff2-1106-4309-a138-56f03535a494&id=76ae85e2-88e5-4e99-83e4-5f352108aebc"
        querystring = {
            "apikey": "59383ff2-1106-4309-a138-56f03535a494",
            "type": "matches"
        }
        response = requests.get(url, params=querystring)
        data = response.json()
        today = datetime.date.today()
        today_matches = [match for match in data["data"]["matchList"] if datetime.datetime.strptime(match["date"], "%Y-%m-%d").date() == today]
        
        if today_matches:
            for match in today_matches:
                match_name = match["name"]
                match_status = match["status"]
                match_venue = match["venue"]
                print(f"{match_name}: {match_status} at {match_venue}")
        else:
            print("No IPL matches scheduled for today.")
    except Exception as e:
        print(f"Error fetching live match scores: {e}")
    
def ask_code(intent):
        genai.configure(api_key="AIzaSyCg7wST5E-kgudcYLu7HQ3F3xu93dMUClE")
        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        convo = model.start_chat(history=[
        ])
        convo.send_message(intent)
        return convo.last.text
    
def get_directions(api_key, intent):
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=api_key)
    
    # Get user's location
    try:
        user_location = gmaps.geolocate()['location']
        origin = f"{user_location['lat']},{user_location['lng']}"
    except Exception as e:
        print(f"Error getting user's location: {e}")
        return "Sorry, couldn't determine user's location."
    
    # Determine destination based on user intent
    destination = get_destination_from_intent(intent)
    if not destination:
        return "Sorry, couldn't understand the destination."
    
    # Calculate directions from origin to destination
    try:
        directions = gmaps.directions(origin, destination, mode="driving")
        if directions:
            # Extract relevant information from the directions response
            route_summary = directions[0]['summary']
            total_distance = directions[0]['legs'][0]['distance']['text']
            total_duration = directions[0]['legs'][0]['duration']['text']
            
            # Construct the directions message
            directions_message = f"To reach {destination}, {route_summary}. "
            directions_message += f"The total distance is {total_distance} and the estimated duration is {total_duration}."
            
            return directions_message
        else:
            return "Sorry, couldn't find directions to the specified destination."
    except Exception as e:
        print(f"Error calculating directions: {e}")
        return "Sorry, couldn't calculate directions at the moment."

def get_destination_from_intent(intent):
    # Define patterns to match destination-related keywords
    destination_patterns = [
        r'to\s+(\w+\s?\w+)',     # Matches "to <destination>"
        r'for\s+(\w+\s?\w+)',     # Matches "for <destination>"
        r'at\s+(\w+\s?\w+)',      # Matches "at <destination>"
        r'(?<=to\s)(\w+\s?\w+)',  # Matches "<destination> to"
        r'(?<=for\s)(\w+\s?\w+)', # Matches "<destination> for"
        r'(?<=at\s)(\w+\s?\w+)'   # Matches "<destination> at"
    ]
    
    # Try matching the patterns with the user's intent
    for pattern in destination_patterns:
        match = re.search(pattern, intent)
        if match:
            # Extract the destination from the matched pattern
            destination = match.group(1)
            return destination.strip()  # Remove leading/trailing whitespace and return
    
    # If no match is found, return None
    return None

# Main program
text = recognize_speech()
# text=input("enter input")
if text:
  translated_text = translate_text(text, 'auto', 'en') 
  print("Translated Text:", translated_text.lower())
  print(execute_intent(translated_text.lower(),'en'))
