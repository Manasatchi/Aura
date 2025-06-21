import json
import time
import random
import requests
import cv2
import numpy as np
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup
from tensorflow import keras
from engine.db import save_emotion_to_db, get_logged_in_user
from engine.command import speak
from empathetic_Luvisa import chat_with_model

# Load model and assets
model = keras.models.load_model('engine/emotion_detection_model.h5')
labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) Chrome/78 Safari/537.36"
]
MAX_RETRIES = 3
RETRY_DELAY = 2

def fetch_tip_from_web(emotion):
    """Fetch first helpful article link from Google."""
    query = f"how to deal with {emotion.lower()} emotions site:psychologytoday.com OR site:medium.com"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    retries = 0

    while retries < MAX_RETRIES:
        try:
            print(f"Fetching online tip for {emotion}...")
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            for link in soup.find_all('a', href=True):
                href = link['href']
                if "url?q=" in href and "webcache" not in href:
                    real_url = href.split("url?q=")[1].split("&")[0]
                    return real_url
            return None

        except requests.exceptions.RequestException as e:
            print(f"Retry {retries + 1}: {e}")
            retries += 1
            time.sleep(RETRY_DELAY)
    return None

def fetch_emotional_support_gpt(emotion):
    """Fetch a supportive tip from Luvisa."""
    prompt = f"I'm feeling {emotion}. Please provide me supportive advice with a practical tip."
    return chat_with_model(prompt)

def monitor_and_provide_real_time_support(duration=600):
    """Monitor emotion live and offer dynamic help if necessary."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Camera not available. Please check and restart.")
        return

    #speak("Starting real-time emotional care session. Please stay visible to me.")
    start_time = time.time()
    last_emotion = "Neutral"
    last_detected_time = time.time()

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        current_emotion = None

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            if face.size == 0:
                continue

            resized = cv2.resize(face, (48, 48)) / 255.0
            reshaped = np.reshape(resized, (1, 48, 48, 1))
            prediction = model.predict(reshaped, verbose=0)
            confidence = np.max(prediction)
            emotion = labels[np.argmax(prediction)]

            if confidence > 0.6:
                current_emotion = emotion
                break  # Focus on first clear face

        if current_emotion:
            print(f"[Detected] Emotion: {current_emotion}")

            user_id = get_logged_in_user()
            if user_id:
                save_emotion_to_db(user_id, current_emotion)

            if (current_emotion not in ['Happy', 'Neutral']) and (current_emotion != last_emotion):
                speak(f"I noticed a change to {current_emotion.lower()} mood. I'm here to support you.")

                # Get GPT advice
                gpt_response = fetch_emotional_support_gpt(current_emotion)
                if gpt_response:
                    speak(gpt_response)

                # Get online resource
                resource_link = fetch_tip_from_web(current_emotion)
                if resource_link:
                    speak("I found a helpful article. Opening it for you.")
                    webbrowser.open(resource_link)
                else:
                    speak("Couldn't fetch an article right now. But remember, you are not alone.")

                last_detected_time = time.time()
                last_emotion = current_emotion

            # Reset if no emotional change detected for a long time
            if time.time() - last_detected_time > 300:
                last_emotion = "Neutral"

        time.sleep(3)  # avoid hammering model predictions

    cap.release()
    cv2.destroyAllWindows()
    speak("Emotional care session ended. Take good care of yourself!")

if __name__ == "__main__":
    monitor_and_provide_real_time_support(duration=600)  # Default: 10 mins session
