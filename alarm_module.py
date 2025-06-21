import threading
import schedule
import datetime
import time
import pyttsx3
import os
from playsound import playsound
from plyer import notification

ALARM_SOUND = "alarm.mp3"
alarms = []  # Holds tuples of (formatted_time, job_id)
lock = threading.Lock()

def speak(text):
    try:
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)
        engine.setProperty("rate", 200)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS error: {e}")

# Trigger function now takes unique job_id
def alarm_trigger(time_str, job_id):
    with lock:
        print(f"🔔 Alarm Triggered for {time_str} (Job ID: {job_id})")
        try:
            speak(f"Alarm ringing for {time_str}")
            notification.notify(
                title="⏰ Alarm!",
                message=f"Alarm set for {time_str} is ringing.",
                timeout=10
            )
            if os.name == 'nt':
                playsound(ALARM_SOUND)
        except Exception as e:
            print(f"Alarm playback error: {e}")
        return schedule.CancelJob

# Generate unique ID for each alarm
def generate_alarm_id():
    return f"job_{int(time.time() * 1000)}"

def set_alarm(time_str):
    try:
        time_str = time_str.strip()
        time_obj = datetime.datetime.strptime(time_str, "%H:%M")
        formatted = time_obj.strftime("%H:%M")

        job_id = generate_alarm_id()
        job = schedule.every().day.at(formatted).do(alarm_trigger, formatted, job_id)
        alarms.append((formatted, job_id, job))

        speak(f"Alarm set for {formatted}")
        print(f"✅ Alarm set for {formatted} (Job ID: {job_id})")
    except ValueError:
        speak("Invalid time format. Please use HH:MM like 06:30.")
        print("❌ Invalid time format")

def list_alarms():
    return [f"{a[0]} (ID: {a[1]})" for a in alarms]

def remove_alarm(job_id):
    global alarms
    for alarm in alarms:
        if alarm[1] == job_id:
            schedule.cancel_job(alarm[2])
            alarms.remove(alarm)
            speak(f"Alarm {job_id} canceled.")
            return True
    speak(f"No alarm found with ID {job_id}")
    return False

def run_alarm_scheduler():
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"Schedule error: {e}")
        time.sleep(1)
