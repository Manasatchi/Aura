from reminder_module import init_db, add_reminder, scheduler_loop, load_reminders
import threading
import os
import eel
import subprocess
from engine.features import *
from engine.command import *
from engine.auth import recoganize
#from luvisha.empathetic_Luvisa import luvisa_call

def start():
    eel.init("www")

    eel.init("web")
    @eel.expose
    def init():
        playAssistantSound()
        subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.authenticate_face()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            greetMe()
            eel.hideStart()
            playAssistantSound()

            init_db()
            load_reminders()
            threading.Thread(target=scheduler_loop, daemon=True).start()

            from alarm_module import run_alarm_scheduler
            threading.Thread(target=run_alarm_scheduler, daemon=True).start()
            
            from auto_call_answer import monitor_incoming_calls
            threading.Thread(target=monitor_incoming_calls, daemon=True).start()
            
            from emotion_prediction import monitor_and_provide_real_time_support
            threading.Thread(target=monitor_and_provide_real_time_support, args=(600,), daemon=True).start()
            
        else:
            speak("Face Authentication Fail")
    
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)
