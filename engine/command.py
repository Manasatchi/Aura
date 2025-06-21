import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from pipes import quote
import pyttsx3
import speech_recognition as sr
import eel
import time
import pyautogui  
from pygame import mixer
from plyer import notification
#from datetime import datetime
from playsound import playsound
from reminder_module import add_reminder
import random
import webbrowser
from PIL import Image
import datetime
import random
import time
import pygame

eel.init("web")
def play_background_music():
    pygame.mixer.init()
    pygame.mixer.music.load("web\\bgm.mp3")
    pygame.mixer.music.play(-1)

def stop_background_music():
    pygame.mixer.music.stop()

def speak_slowly(text):
    # Speaking with pauses between each word
    words = text.split()
    for word in words:
        speak(word)
        time.sleep(1)  # Pause between each word for natural feel

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    print(f"Assistant: {text}")
    eel.receiverText(text)
    
    engine.runAndWait()

def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening....')
        eel.DisplayMessage('Listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('Recognizing')
        eel.DisplayMessage('Recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

#univerasl open function
        if "open" in query:   #EASY METHOD
                query = query.replace("open","")
                query = query.replace("jarvis","")
                speak(f"Opening {query.strip()}")
                pyautogui.press("super")
                pyautogui.typewrite(query)
                pyautogui.sleep(2)
                pyautogui.press("enter") 

#message function
        elif "send message" in query or "phone call" in query or "video call" in query or " make a video call" in query or " make a call" in query or "call" in query:
            from engine.features import findContact, whatsAppMessage, makeCall, sendMessage, makeWhatsAppVoiceCall, makeWhatsAppVideoCall
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query or " make a call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")

                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = takecommand()
                        speak("what message to send")
                        query = takecommand()
                        whatsAppMessage(message, contact_no, name)

                    elif "phone call" in query or " make a call" in query or " call" in query:
                        makeWhatsAppVoiceCall(name, contact_no)

                    elif "video call" in query or " make a video call" in query:
                        makeWhatsAppVideoCall(name, contact_no)
                    
                    else:
                        speak("sorry,something went wrong")
                        
                    whatsAppMessage(contact_no, query, message, name)

#Gendral Questions
        elif "hello" in query or "hai" in query or "hi" in query:
            greetings = [
                "Hello sir! It's always a pleasure to hear from you.",
                "Hi sir! Ready when you are.",
                "Greetings, sir! What can I help you with today?",
                "Hello, sir! Fully operational and standing by."
            ]
            speak(random.choice(greetings))
        
        elif "i am fine" in query or "am fine" in query or "i'm fine" in query:
            responses = [
                "That's wonderful to hear, sir!",
                "Great! Let's make your day even better.",
                "I'm glad you're doing well, sir.",
                "Awesome, sir. Let’s keep up the positive energy!"
            ]
            speak(random.choice(responses))
        
        elif "how are you" in query:
            replies = [
        "I'm performing at optimal capacity, sir!",
        "Doing perfectly, thanks for asking. Let’s get to work!",
        "Feeling sharp and ready, sir!",
        "I'm in top form, sir — always ready to assist."
            ]
            speak(random.choice(replies))

        elif "thank you" in query:
            replies = [
        "You're most welcome, sir!",
        "Happy to help anytime.",
        "No thanks needed, sir. That’s what I’m here for.",
        "At your service, always."
            ]
            speak(random.choice(replies))

        elif "about yourself" in query or "about yourself" in query:
            intros = [
        "It’s my pleasure, sir. I am Aura — your smart personal assistant, designed to support you with any task, anytime.",
        "I’m Aura, your dedicated assistant — optimized for productivity, clarity, and responsiveness.",
        "Sir, I am Aura — built to assist, enhance, and simplify your digital experience with intelligence and efficiency.",
        "As Aura, my mission is to anticipate your needs, answer your questions, and make your life easier through technology."
            ]
            speak(random.choice(intros))

        elif "translate" in query.lower():
            from engine.features import translategl
    # Remove unnecessary words from the query
            query = query.replace("aura", "")  
            query = query.replace("translate", "")  
            query = query.strip()  # Remove extra spaces if any
    # Call the translategl function to process translation
            translategl(query)

        elif "tired" in query or "am tired" in query or "am just tired" in query:
                    speak("Playing your favourite songs, sir")
                    a = (1,2,3) # You can choose any number of songs (I have only choosen 3)
                    b = random.choice(a)
                    if b==1:
                        webbrowser.open("https://youtu.be/8jhC9xnJGYU?si=ATrKQSoiFUNPs54n")
                    elif b==2:
                        webbrowser.open("https://youtu.be/eNX9VqUzBco?si=XTMNzfuROPiBXM0v")
                    elif b==3:
                        webbrowser.open("https://youtu.be/dD3k-tswGd0?si=haEJOXtZ6lCbkBbG")


        elif "the time now" in query.lower() or "what's the time now" in query.lower() or "time now" in query.lower():
            now = datetime.datetime.now()
            strTime = now.strftime("%I:%M %p")  # e.g., 03:30 PM
            hour = now.strftime("%I").lstrip("0") or "12"
            minute = now.strftime("%M")
            meridian = now.strftime("%p")

    # Greeting based on time
            if now.hour < 12:
                    part_of_day = "morning"
            elif 12 <= now.hour < 17:
                    part_of_day = "afternoon"
            else:
                part_of_day = "evening"

    # Dynamic speaking sentences
                time_responses = [
        f"The current time is {hour}:{minute} {meridian}. Good {part_of_day}!",
        f"It's exactly {hour}:{minute} {meridian}. Hope you're having a great {part_of_day}.",
        f"Right now, it's {hour}:{minute} {meridian}. Enjoy your {part_of_day}!",
        f"Time check: {hour}:{minute} {meridian}. Wishing you a wonderful {part_of_day}!",
        f"The clock shows {hour}:{minute} {meridian}. Lovely {part_of_day} to you!"
    ]
    
            response = random.choice(time_responses)
            speak_slowly(response)
            print(f"🕒 {strTime} - {part_of_day.capitalize()}")


        elif "temperature" in query.lower():
            from engine.features import get_weather_info
            speak("Which location should I check the temperature for?")
            location = takecommand().lower()
            if location and location != "none":
                    get_weather_info(location, type="temperature")
            else:
                    speak("I didn't catch the location. Please try again.")

        elif "weather" in query.lower():
            from engine.features import get_weather_info
            speak("Which location do you want the weather for?")
            location = takecommand().lower()
            if location and location != "none":
                get_weather_info(location, type="weather")
            else:
                speak("Sorry, please say the location again.")


#camera function
        elif "click my photo" in query or "selfie" in query :
            pyautogui.press("super")
            pyautogui.typewrite("camera")
            pyautogui.press("enter")
            pyautogui.sleep(2)
            #speak("Opening camera")
            speak("SAY Cheeeese!")
            pyautogui.press("enter")

#Searching through various platform
        elif "google" in query or "search on google" in query or "search" in query:
                from engine.features import searchGoogle
                searchGoogle(query)

        elif "wikipedia" in query:
                from engine.features import searchWikipedia
                searchWikipedia(query)

        elif "youtube" in query or "search on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

#daily remainders and task notification
        elif "set a reminder" in query or "remind me" in query:
            speak("What should I remind you about?")
            task = takecommand()
            speak("At what time? Please say it in HH:MM format")
            time_str = takecommand()
            speak("Should I repeat it daily, hourly, or once?")
            repeat = takecommand()

            add_reminder(task, time_str, repeat)
            speak(f"Okay! I will remind you to {task} at {time_str} every {repeat}.")

#alarm
        elif "set an alarm" in query:
            speak("What time should I set the alarm for?")
            alarm_raw = takecommand().lower().strip()
            alarm_raw = alarm_raw.replace("colon", ":").replace(" ", "")
    
            import re
            match = re.match(r"^(\d{1,2}):?(\d{2})$", alarm_raw)
            if match:
                hh, mm = match.groups()
                alarm_time = f"{int(hh):02}:{int(mm):02}"
                from alarm_module import set_alarm
                set_alarm(alarm_time)
            else:
                speak("Sorry, I couldn't understand the time. Please try again.")
        
        elif "list alarms" in query:
            from alarm_module import list_alarms
            alarms = list_alarms()
            if alarms:
                for t in alarms:
                    speak(f"Alarm set for {t}")
            else:
                speak("No alarms set.")

        elif "cancel alarm" in query:
            speak("Which time should I cancel?")
            time_to_cancel = takecommand().replace("colon", ":").replace(" ", "").strip()
            from alarm_module import remove_alarm
            removed = remove_alarm(time_to_cancel)
            if removed:
                print(f"Canceled alarm for {time_to_cancel}")

#media control
        elif "ipl score" in query.lower():
            from engine.features import get_ipl_score
            speak("Getting the latest IPL score...")
            get_ipl_score()


        elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup()
        elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()
        
#llama 3.3
        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("error")
    
    eel.ShowHood()