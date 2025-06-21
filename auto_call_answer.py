import os
import time
import subprocess
import threading
import datetime
import sounddevice as sd
from scipy.io.wavfile import write

# ========== SETTINGS ==========
USE_ADB = True
RECORD_DURATION = 90
WAIT_BEFORE_ANSWER = 20
WHATSAPP_CLICK_POS = (1350, 250)
TTS_MESSAGE = "Sorry, I am busy right now. Please call me later."
LAPTOP_RECORD_DIR = "call_recordings"
PHONE_RECORD_DIR = "/storage/emulated/0/call_speech_aura/Call_Recordings"
DEBOUNCE_SECONDS = 15
last_trigger_time = 0
# ===============================

def speak_on_phone(text):
    try:
        print("[INFO] Speaking message via Android TTS...")

        # Save message to a temp file on the device
        tts_script = f"""
        text="{text}"
        echo $text | am startservice --user 0 -a com.google.android.tts.service.ACTION_SPEAK --es text "$text" --es lang "en-US"
        """
        command = f'adb shell "echo \\"{text}\\" > /sdcard/tts_message.txt && service call texttospeech 7 i32 0 s16 \\"{text}\\""'
        
        os.system(command)
        print(f"[TTS] Sent message to Google TTS: {text}")

    except Exception as e:
        print(f"[ERROR] TTS failed: {e}")


def send_phone_notification(title, text):
    try:
        # This works on Android 9+ without Termux
        command = f'adb shell cmd notification post -S bigtext -t "{title}" "aura.notification" "{text}"'
        os.system(command)
        print(f"[NOTIFY] Notification posted: {title} - {text}")
    except Exception as e:
        print(f"[ERROR] Notification failed: {e}")


def answer_call_adb():
    os.system("adb shell input keyevent KEYCODE_HEADSETHOOK")
    print("[ACTION] Call answered via ADB")


def answer_whatsapp_call():
    import pyautogui
    x, y = WHATSAPP_CLICK_POS
    pyautogui.click(x, y)
    print("[ACTION] WhatsApp call answered")


def record_and_save_call(duration=RECORD_DURATION):
    fs = 44100
    os.makedirs(LAPTOP_RECORD_DIR, exist_ok=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"call_{now}.wav"
    laptop_path = os.path.join(LAPTOP_RECORD_DIR, filename)

    print("[REC] Recording started...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write(laptop_path, fs, audio)
    print(f"[REC] Saved to: {laptop_path}")

    phone_path = os.path.join(PHONE_RECORD_DIR, filename).replace("\\", "/")
    os.system(f"adb shell mkdir -p {PHONE_RECORD_DIR}")
    os.system(f'adb push "{laptop_path}" "{phone_path}"')
    print(f"[SYNC] Pushed to phone: {phone_path}")

    send_phone_notification("Call Recording Saved", f"Saved to: {phone_path}")


def auto_call_assistant():
    global last_trigger_time
    print(f"[WAIT] {WAIT_BEFORE_ANSWER}s before answering...")
    time.sleep(WAIT_BEFORE_ANSWER)

    if USE_ADB:
        answer_call_adb()
    else:
        answer_whatsapp_call()

    time.sleep(2)
    speak_on_phone(TTS_MESSAGE)

    threading.Thread(target=record_and_save_call, args=(RECORD_DURATION,), daemon=True).start()
    print(f"[SIM] Call ongoing for {RECORD_DURATION}s...")
    time.sleep(RECORD_DURATION)


def monitor_incoming_calls():
    global last_trigger_time
    print("[MONITOR] Watching for real incoming calls...")

    while True:
        print("[ADB] Clearing logcat...")
        os.system("adb logcat -c")
        time.sleep(1)

        process = subprocess.Popen(["adb", "logcat", "-v", "brief"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding='latin-1')

        try:
            for line in process.stdout:
                if ("Telecom" in line or "Telephony" in line) and "RINGING" in line:
                    current_time = time.time()
                    if current_time - last_trigger_time > DEBOUNCE_SECONDS:
                        last_trigger_time = current_time
                        print(f"[CALL DETECTED] {line.strip()}")
                        threading.Thread(target=auto_call_assistant, daemon=True).start()
                        break
        except Exception as e:
            print(f"[ERROR] Logcat read failed: {e}")
        finally:
            process.terminate()
            time.sleep(1)


if __name__ == "__main__":
    monitor_incoming_calls()
