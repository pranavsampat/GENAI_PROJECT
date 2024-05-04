import speech_recognition as sr
import subprocess

# Function to recognize speech using Google Speech Recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        return "Sorry, I could not understand what you said."
    except sr.RequestError as e:
        return f"Sorry, could not request results from Google Speech Recognition service; {e}"

# Function to execute actions based on user's intent
def execute_intent(text):
    if "open google" in text:
        subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])  # Replace with actual path
        return "Opening Google Chrome..."
    elif "show me images" in text:
        # Code to show images (e.g., using a library like PIL)
        return "Showing images..."
    elif "how are you" in text:
        return "I'm fine, thank you!"
    else:
        return "Sorry, I'm not sure what you're asking for."

# Main loop
while True:
    speech = recognize_speech()
    print("You said:", speech)
    response = execute_intent(speech)
    print("Bot:", response)
