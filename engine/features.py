import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipes import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine
import pywhatkit
import wikipedia
import datetime
import random
import googletrans #pip install googletrans
from gtts import gTTS
from googletrans import Translator , LANGUAGES
import speech_recognition
from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat
import requests
from bs4 import BeautifulSoup
from plyer import notification

con = sqlite3.connect("aura.db")
cursor = con.cursor()

@eel.expose
def playAssistantSoundsound():
    music_dir = "www\\assets\\audio\\intro.mp3"
    playsound(music_dir)

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis","")
        query = query.replace("google search","")
        query = query.replace("google","")
        speak("This is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query,1)
            speak(result)

        except:
            speak("No speakable output available")

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from wikipedia....")
        query = query.replace("wikipedia","")
        query = query.replace("search wikipedia","")
        query = query.replace("jarvis","")
        results = wikipedia.summary(query,sentences = 2)
        speak("According to wikipedia..")
        print(results)
        speak(results)

def Playyoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!") 
        query = query.replace("youtube search","")
        query = query.replace("youtube","")
        query = query.replace("jarvis","")
        web  = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done Sir!")
        
def greetMe():
    hour  = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        morning_greetings = [
            "Good morning, sir! Hope you're feeling refreshed and ready to go.",
            "A very good morning, sir! Let's make today a great one.",
            "Good morning, sir! I'm all set to help you conquer your goals.",
            "Rise and shine, sir! Ready to start the day?",
            "Top of the morning to you, sir! What’s on the agenda today?"
        ]
        speak(random.choice(morning_greetings))

    elif 12 <= hour < 17:
        afternoon_greetings = [
            "Good afternoon, sir! I hope your day is going great. I'm fully ready to assist you.",
            "A warm good afternoon, sir! How can I make your day smoother?",
            "Good afternoon! I'm here and at your service, sir.",
            "Hope you're having a productive afternoon, sir! Let me know how I can help.",
            "Good afternoon, sir! Let's keep the momentum going strong.",
            "Wishing you a fantastic afternoon, sir! I'm all set and standing by."
        ]
        speak(random.choice(afternoon_greetings))

    elif 17 <= hour < 21:
        evening_greetings = [
            "Good evening, sir! I hope you had a productive day. How can I assist you now?",
            "A peaceful evening to you, sir! Ready to wind down or keep going?",
            "Good evening, sir! I’m still here with you — let’s finish strong.",
            "Welcome back, sir. I trust your day went well. How can I help this evening?",
            "Evening vibes, sir! Let me take care of what’s left for today.",
            "Good evening, sir! Always here to make your evening smoother and smarter."
        ]
        speak(random.choice(evening_greetings))

    else:
        night_greetings = [
            "It’s late, sir. But I’m still here if you need anything.",
            "Good night, sir! Don’t forget to rest and recharge.",
            "Late hours, sir? I admire your dedication. How can I assist?",
            "The night is quiet, but I'm still listening, sir.",
            "Wishing you a peaceful night, sir. Let me know if you need help before bed."
        ]
        speak(random.choice(night_greetings))

    #speak("Please tell me, How can I help you?")
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
    
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["aura","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

# import subprocess
# import time
# import pyautogui
# from urllib.parse import quote

# def speak(message):
#     print(message) 

# def whatsApp(mobile_no, message, flag, name):
#     if flag == 'message':
#         target_tab = 12  # Message box (where you type the message)
#         jarvis_message = "Message sent successfully to " + name
#         pyautogui.press("enter")  # Press enter to send the message (after focusing on the message box)
#         target_tab = 13  # Adjust if necessary for different actions after sending

#     elif flag == 'call':
#         target_tab = 5  # Audio call button
#         message = ''
#         jarvis_message = "Calling to " + name

#     elif flag == 'video_call':
#         target_tab = 6  # Video call button
#         message = ''
#         jarvis_message = "Starting video call with " + name

#     # Encode the message for URL (optional, if needed for URL-safe encoding)
#     encoded_message = quote(message)
#     print(encoded_message)
    
#     # Construct the WhatsApp URL
#     whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

#     # Construct the full command to open WhatsApp
#     full_command = f'start "" "{whatsapp_url}"'

#     # Open WhatsApp with the constructed URL using cmd.exe
#     subprocess.run(full_command, shell=True)
#     time.sleep(5)

#     # Re-run to open WhatsApp again (if necessary)
#     subprocess.run(full_command, shell=True)
    
#     # Simulate CTRL + F to focus the search box in WhatsApp Web (if needed)
#     pyautogui.hotkey('ctrl', 'f')

#     # Simulate tabbing through the target element (message box, call button, etc.)
#     for i in range(1, target_tab):
#         pyautogui.hotkey('tab')  # Navigate to the target tab (message, call, etc.)

#     # Now, click the Enter button directly using its coordinates (replace with the actual ones)
#     enter_button_x = 1000  # Example X coordinate
#     enter_button_y = 800   # Example Y coordinate
#     pyautogui.click(enter_button_x, enter_button_y)  # Click the Enter button

#     # Print a message via the "speak" function (you can replace this with TTS)
#     speak(jarvis_message)



def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)

    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import os
import time

def translategl(query):
    try:
        # Initialize the Translator
        translator = Translator()
        
        # List of available languages
        print("Available languages for translation:", translator.LANGUAGES)
        
        # Prompt user for the target language
        speak("Sure sir, choose the language in which you want to translate.")
        b = input("Enter target language code (e.g., 'en' for English, 'es' for Spanish, etc.): ")
        
        # Validate language code
        if b not in translator.LANGUAGES:
            speak("Sorry, the language code you entered is invalid. Please try again.")
            return

        # Translate the query text
        text_to_translate = translator.translate(query, src="auto", dest=b)
        text = text_to_translate.text
        
        # Convert translated text to speech using gTTS
        speakgl = gTTS(text=text, lang=b, slow=False)
        
        # Save the speech to a file and play it
        speakgl.save("voice.mp3")
        playsound("voice.mp3")
        
        # Clean up by removing the temporary mp3 file
        time.sleep(5)
        os.remove("voice.mp3")
        
        print(f"Translation: {text}")
        speak(f"Translation is: {text}")
    
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, there was an error in translation. Please try again.")


API_KEY = "4fafbc914800e7f71f9df73b08586583"  # Replace with your actual API key

def get_weather_info(location, type="weather"):
    try:
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(base_url)
        data = response.json()

        if data["cod"] != 200:
            speak(f"Sorry, I couldn't find weather data for {location}.")
            print(f"[ERROR] {data.get('message', 'Unknown error')}")
            return

        if type == "temperature":
            temp = data["main"]["temp"]
            speak(f"The current temperature in {location} is {temp} degrees Celsius.")
            print(f"[INFO] Temperature in {location}: {temp}°C")

        elif type == "weather":
            desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            speak(f"The weather in {location} is {desc} with a temperature of {temp}°C, humidity of {humidity} percent, and wind speed of {wind} meters per second.")
            print(f"[INFO] Weather in {location}: {desc}, Temp: {temp}°C, Humidity: {humidity}%, Wind: {wind} m/s")

    except Exception as e:
        speak("Sorry, something went wrong while fetching the weather.")
        print(f"[ERROR] Weather fetch failed: {e}")

def get_ipl_score():
    try:
        url = "https://www.iplt20.com/"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        # Find the live match section
        live_match_section = soup.find("div", class_="cb-col cb-col-100 cb-ltst-wgt-hdr")

        if not live_match_section:
            print("[ERROR] Live match section not found.")
            notification.notify(title="IPL Score", message="No live matches found.", timeout=10)
            return

        # Get team names and scores
        team_names = live_match_section.find_all("div", class_="cb-ovr-flo cb-hmscg-tm-nm")
        team_scores = live_match_section.find_all("div", class_="cb-ovr-flo")

        if len(team_names) >= 2 and len(team_scores) >= 11:
            team1 = team_names[0].text.strip()
            team2 = team_names[1].text.strip()
            team1_score = team_scores[8].text.strip()
            team2_score = team_scores[10].text.strip()

            message = f"{team1} : {team1_score}\n{team2} : {team2_score}"
            print(message)

            notification.notify(
                title="Live IPL Score",
                message=message,
                timeout=15
            )
        else:
            print("[ERROR] Couldn't extract team names or scores.")
            notification.notify(title="IPL Score", message="Could not parse score.", timeout=10)

    except Exception as e:
        print(f"[ERROR] Failed to fetch score: {e}")
        notification.notify(title="IPL Score", message="Something went wrong.", timeout=10)

# Call the function
get_ipl_score()

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    #return response

# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)

# to send message | all the whatsapp & sms function are only working for infinix note 30 interface
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    tapEvents(-12, -169)
    # open sms app
    tapEvents(314, 2275)
    #start chat
    tapEvents(923, 2293)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 1344)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1347)
    speak("message send successfully to "+name)

def whatsAppMessage(message, mobile_no, name):
    # Import necessary helper functions
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    # Pre-process the message and mobile number (replace spaces with '%')
    message = replace_spaces_with_percent_s(message)
    mobile_no = replace_spaces_with_percent_s(mobile_no)
    # Speak message for user feedback
    speak("Sending WhatsApp message")
    # Go back 4 steps in the app navigation (adjust as needed for your app)
    goback(4)
    time.sleep(1)
    # Simulate key event (e.g., home button or back button)
    keyEvent(3)  # Simulate pressing the home button (Key event 3 is the home button in ADB)
    # Tap the WhatsApp icon (adjust coordinates based on your screen resolution)
    tapEvents(714, 2317)
    # Wait for the app to open (adjust timing if necess ary)
    time.sleep(2)
    # Tap on the search bar to start a new chat
    tapEvents(400, 363)  
    # Wait for the search field to appear
    time.sleep(1)
    # Search for the mobile number (replace spaces with '%20' if needed)
    adbInput(mobile_no)  
    # Wait for the search result to appear
    time.sleep(1)
    # Tap on the contact's name (adjust coordinates to match the contact's name)
    tapEvents(274, 701) 
    # Tap on the input area to start typing the message
    tapEvents(208, 2384)  
    # Input the actual message text using ADB input (message is pre-processed to replace spaces)
    adbInput(message)
    # Tap on the send button to send the message (adjust the coordinates for the send button)
    tapEvents(955, 1391)  #1009, 2381
    # Speak back to confirm the message has been sent
    speak("Message sent successfully to " + name)
#1009, 2381


def makeWhatsAppVoiceCall(name,mobile_no):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    mobile_no = replace_spaces_with_percent_s(mobile_no)
    #mobile_no = mobile_no.replace(" ", "")
    speak(f"Calling {name} via WhatsApp voice call")
    
    goback(4)  # Go back to home (optional if needed)
    time.sleep(1)

    # Tap the WhatsApp icon (adjust coordinates based on your screen resolution)
    tapEvents(714, 2317)
    # Wait for the app to open (adjust timing if necess ary)
    time.sleep(2)
    # Tap on the search bar to start a new chat
    tapEvents(400, 363)  
    # Wait for the search field to appear
    time.sleep(1)
    # Search for the mobile number (replace spaces with '%20' if needed)
    adbInput(mobile_no)  
    # Wait for the search result to appear
    time.sleep(4)
    # Tap on the contact's name (adjust coordinates to match the contact's name)
    tapEvents(882, 209) 
    # Tap on the voice call button
    tapEvents(208, 2384)  

def makeWhatsAppVideoCall(name, mobile_no):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    mobile_no = replace_spaces_with_percent_s(mobile_no)
    speak(f"Calling {name} via WhatsApp video call")
    
    goback(4)  # Go back to home (optional if needed)
    time.sleep(1)

    # Tap the WhatsApp icon (adjust coordinates based on your screen resolution)
    tapEvents(714, 2317)
    # Wait for the app to open (adjust timing if necess ary)
    time.sleep(2)
    # Tap on the search bar to start a new chat
    tapEvents(400, 363)  
    # Wait for the search field to appear
    time.sleep(1)
    # Search for the mobile number (replace spaces with '%20' if needed)
    adbInput(mobile_no)  
    # Wait for the search result to appear
    time.sleep(4)
    # Tap on the contact's name (adjust coordinates to match the contact's name)
    tapEvents(882, 209) 
    # Tap on the video call button
    tapEvents(753, 191)  

