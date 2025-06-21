
# 🌌 Aura — Emotion-Aware AI Assistant with Voice Interface & Automation

**Aura** is an advanced, modular AI-powered personal assistant designed to understand and support users emotionally and functionally. It combines voice recognition, emotion detection, web-based interaction, auto call handling via ADB, alarms, reminders, and empathetic responses. Built using Python, web technologies (HTML, CSS, JS), and machine learning, Aura strives to act as an intelligent, emotionally responsive digital companion.

---

## 📁 Project Structure

```
Aura/
│
├── engine/                      # Backend engine logic and utilities
├── www/                         # Web UI files (HTML, CSS, JS)
│
├── alarm.mp3                    # Default alarm sound
├── aura.db                      # SQLite database for persistent storage
├── device.bat                   # Batch file to manage device interface (e.g., ADB)
│
├── alarm_module.py              # Alarm functionality
├── alert.py                     # Visual/audio alert system
├── auto_call_answer.py          # Auto answer phone calls using ADB
├── emotion_prediction.py        # Emotion detection using ML models
├── empathetic_Luvisa.py         # Core AI assistant logic with empathy
├── main.py                      # Central initializer (can be used as main entry)
├── reminder_module.py           # Reminder management
├── run.py                       # Main execution script
│
└── .gitignore                   # Git ignored files
```

---

## 🧠 Features Overview

### 🎙️ Voice Assistant with Empathy
- Uses microphone input for natural voice interaction.
- Responds empathetically using emotion detection via facial expressions and tone analysis.
- Integrated with `Luvisa`, a personality-driven response system.

### 🤖 Emotion Detection
- Built-in emotion recognition via facial expression analysis.
- Triggers appropriate responses and adjustments in behavior based on user emotion.

### 📱 Auto Call Answering (via ADB)
- Automatically detects and answers incoming calls.
- Pushes audio responses and logs information.
- Uses `auto_call_answer.py` with ADB shell commands for Android devices.

### ⏰ Alarm & Reminder System
- Set alarms using natural commands.
- Plays sound (e.g., `alarm.mp3`) and can be triggered via scheduled tasks.
- Reminder module allows creation of timely reminders stored in `aura.db`.

### 🌐 Web Interface
- Web-based GUI built using HTML/CSS/JavaScript inside the `/www` folder.
- Interfaces with backend for real-time updates, emotion display, and interaction.
- Can display alerts, reminders, and assistant dialogues visually.

---

## 🛠️ Tech Stack

| Area                     | Technology                            |
|--------------------------|----------------------------------------|
| 💬 Voice Recognition     | `SpeechRecognition`, `pyaudio`         |
| 🧠 ML / Emotion Analysis | OpenCV, `scikit-learn`, NumPy, custom ML models |
| 🔉 Audio Response        | `gTTS`, `playsound`, `pygame`          |
| 📱 Phone Control         | ADB (Android Debug Bridge)             |
| 🗃️ Storage              | SQLite (`aura.db`)                     |
| 🌐 Web Interface         | HTML, CSS, JavaScript, Flask/Eel       |
| 🔁 Background Services   | Python Threads, Scheduling             |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Manasatchi/Aura.git
cd Aura
```

### 2. Install Dependencies

Make sure you have Python 3.8+ and pip installed.

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install manually:

```bash
pip install opencv-python gTTS playsound SpeechRecognition flask pygame numpy
```

### 3. Enable ADB (for phone features)

Ensure USB debugging is enabled on your Android device.

```bash
# Start ADB server
adb start-server

# Connect device
adb devices
```

---

### 4. Run the Assistant

Start the assistant using:

```bash
python run.py
```

This initializes:
- Voice input
- Emotion detection
- Assistant engine (`empathetic_Luvisa.py`)
- Web interface (if integrated)

---

## 📷 Snapshots

Here is a sample UI snapshot of Aura's web interface:

![Aura UI Snapshot](./7fa81dee-c8a9-4e18-afe8-de5676ed1222.png)

---

## 📦 Modules in Detail

### 🧩 `empathetic_Luvisa.py`
The emotional core of Aura. It processes user input, checks emotional state, and formulates natural responses. Integrates TTS and optional facial expression feedback.

### 🤖 `emotion_prediction.py`
Detects user emotion using webcam input and ML model. Returns predictions like "happy", "sad", "angry", which then influence the assistant's tone.

### 📱 `auto_call_answer.py`
Auto-answers calls using ADB for Android devices. Can simulate pressing answer, play a message, and record responses.

### ⏰ `alarm_module.py` & `reminder_module.py`
Used to schedule alarms and reminders. The alarms use audio triggers and optional alerts in the web interface.

### 🔊 `alert.py`
Can flash alerts or play sounds for urgent notifications.

---

## 🔐 Database

**aura.db** stores:
- Reminder entries
- Emotional logs (optional)
- Assistant preferences
- Call handling logs

You can inspect or edit using any SQLite viewer.

---

## 🖼️ Web Interface

Files in `www/` provide a simple but interactive UI for:
- Displaying assistant dialogues
- Showing emotional responses
- Controlling basic settings

You can run the Flask/Eel server (depending on the method you’ve wired) to host the UI locally.

---

## 🧪 Use Cases

| Scenario                       | Feature Used                         |
|--------------------------------|--------------------------------------|
| Emotionally stressed user      | Empathetic response + calming alert  |
| Missed medication or meetings  | Reminder + Alert                     |
| User receives a call while busy| Auto-answer with pre-recorded message|
| Needing motivation or support  | AI dialogue + emotion-based response |
| Voice-activated commands       | Mic input + NLP                      |

---

## 📌 To-Do / Future Enhancements

- [ ] Add facial recognition to identify users.
- [ ] Sync reminders with Google Calendar.
- [ ] Implement multilingual support.
- [ ] Add sentiment analysis to text input.
- [ ] WebRTC-based video call monitoring.

---

## 🤝 Contributing

Feel free to fork and contribute to Aura! Pull requests are welcome.

### Suggestions

1. Improve ML model accuracy.
2. Enhance web interface with React or Vue.
3. Create mobile companion app.

---

## 🧑‍💻 Author

**DHANASEKAR**  
A passionate AI and automation developer.  
🔗 [GitHub Profile](https://github.com/Manasatchi)
🔗 [LinkedIn Profile](www.linkedin.com/in/dhanasekar-v786)
---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

## 📸 screeshots
![Screenshot 2025-05-02 151842](https://github.com/user-attachments/assets/07363368-c591-492a-a14e-9cb5b03acec2)
![Screenshot 2025-05-20 101712](https://github.com/user-attachments/assets/931bcfdc-c540-4a2c-bb05-67e79d5b5218)
![Screenshot 2025-05-20 104506](https://github.com/user-attachments/assets/2cd8ba72-bced-4835-895e-fdd5e5a2bcbc)
![Screenshot 2025-05-01 171823](https://github.com/user-attachments/assets/202c864a-c931-4464-a8d8-52c3a4ee2099)



