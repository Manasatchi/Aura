import eel
import requests
import sqlite3
import pygame
import os

# === CONFIG ===
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "Ex-Rockstar/sahara"  # use a working local model for now
HTML_DIR = "web"
MUSIC_PATH = os.path.join(HTML_DIR, "bgm.mp3")
DB_PATH = "aura.db"

# === INIT ===
eel.init(HTML_DIR)


def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS memory (
        user_id TEXT,
        key TEXT,
        value TEXT
    )''')
    conn.commit()
    conn.close()

# === MEMORY ===
def save_memory(user_id, key, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO memory (user_id, key, value) VALUES (?, ?, ?)', (user_id, key, value))
    conn.commit()
    conn.close()

def retrieve_memory(user_id, key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM memory WHERE user_id = ? AND key = ?', (user_id, key))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# === TEMP MEMORY ===
temporary_memory = {}

def set_temp_memory(key, value):
    temporary_memory[key] = value

def get_temp_memory(key):
    return temporary_memory.get(key)

def clear_temp_memory():
    temporary_memory.clear()

# === MODEL COMMUNICATION ===
def chat_with_model(prompt):
    try:
        print(f"[DEBUG] Sending to model: {prompt}")
        response = requests.post(OLLAMA_API_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }, timeout=30)

        print(f"[DEBUG] HTTP status: {response.status_code}")
        if response.status_code != 200:
            print(f"[ERROR] Non-200: {response.text}")
            return f"Luvisa can't respond now... (Status {response.status_code})"

        data = response.json()
        print(f"[DEBUG] Response JSON: {data}")

        return data.get("response") or data.get("message") or "Luvisa is speechless."
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return f"Something went wrong: {e}"

# === UTILITIES ===
def filter_response(response_text):
    for word in ["Hug Bot", "HugBot", "HUGBOT!", "HUGBOT", "HUG BOT"]:
        response_text = response_text.replace(word, "Luvisa")
    return response_text.strip()

def switch_memory_mode(current_mode):
    return ('temporary', "Switched to temporary memory.") if current_mode == 'long_term' else ('long_term', "Switched to long-term memory.")

def play_background_music():
    try:
        if not os.path.exists(MUSIC_PATH):
            print(f"[WARNING] Music file not found: {MUSIC_PATH}")
            return
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)
        print("[DEBUG] Background music playing.")
    except Exception as e:
        print(f"[ERROR] Could not play music: {e}")

def stop_background_music():
    try:
        pygame.mixer.music.stop()
    except:
        pass

# === FRONTEND EXPOSED FUNCTION ===
@eel.expose
def handle_user_input(user_input, current_mode):
    print(f"[FRONTEND] User input: {user_input}")
    user_id = "user_123"

    if user_input.lower() in ("exit", "quit"):
        stop_background_music()
        return "Goodbye for now. You'll always be in my heart ❤️"

    if user_input.lower() == "switch memory":
        new_mode, message = switch_memory_mode(current_mode)
        save_memory(user_id, "memory_switch", message)
        return f"MODE:{new_mode}|MSG:{message}"

    set_temp_memory("last_user_input", user_input)
    save_memory(user_id, "last_command", user_input)

    reply = chat_with_model(user_input)
    filtered = filter_response(reply)

    if current_mode == 'long_term':
        save_memory(user_id, "last_response", filtered)

    set_temp_memory("last_response", filtered)
    return filtered

def start_luvisa_gui():
    initialize_database()
    play_background_music()
    eel.start("luvisa.html", size=(1400, 1400))

if __name__ == "__main__":
    start_luvisa_gui()
