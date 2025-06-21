# reminder_module.py

import sqlite3
import schedule
from datetime import datetime
from plyer import notification
from playsound import playsound
import pyttsx3

engine = pyttsx3.init()

def init_db():
    conn = sqlite3.connect("aura.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY AUTOINCREMENT,task TEXT,time TEXT,repeat TEXT)''')
    conn.commit()
    conn.close()

def notify(task):
    print(f"[🔔 Reminder] {task}")
    playsound("www\\assets\\audio\\reminder.mp3")
    notification.notify(title='Reminder', message=task, timeout=5)
    engine.say(f"Reminder: {task}")
    engine.runAndWait()

def schedule_reminder(task, t_str, repeat):
    if repeat == 'daily':
        schedule.every().day.at(t_str).do(notify, task=task)
    elif repeat == 'hourly':
        schedule.every().hour.at(t_str).do(notify, task=task)
    elif repeat == 'once':
        def one_time_notify():
            if datetime.now().strftime('%H:%M') == t_str:
                notify(task)
                return schedule.CancelJob
        schedule.every(1).minutes.do(one_time_notify)

def load_reminders():
    conn = sqlite3.connect("aura.db")
    c = conn.cursor()
    reminders = c.execute("SELECT task, time, repeat FROM reminders").fetchall()
    conn.close()
    for task, t_str, repeat in reminders:
        schedule_reminder(task, t_str, repeat)

def add_reminder(task, time_str, repeat):
    conn = sqlite3.connect("aura.db")
    c = conn.cursor()
    c.execute("INSERT INTO reminders (task, time, repeat) VALUES (?, ?, ?)", (task, time_str, repeat))
    conn.commit()
    conn.close()
    schedule_reminder(task, time_str, repeat)

def scheduler_loop():
    import time
    while True:
        schedule.run_pending()
        time.sleep(1)