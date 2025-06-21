import requests
from winotify import Notification, audio
import time
import schedule
import os

# ========== SETTINGS ==========  
ICON_PATH = "www\\assets\\img\\logo2.ico"  # <-- Your custom icon path
NOTIFY_INTERVAL_MINUTES = 480  # How often to re-check (in minutes)
KEYWORDS_TO_SEARCH = ['happy life', 'job vacancy bangalore', 'internship', 'tech careers', 'job']  # Default keywords to search
SERP_API_KEY = '0be5841658d6cf5c2f96d37b2f67956afab8d90b531993ca81f2e9dd305e4f39'  # Replace with your SerpApi key
# ===============================

# Function to show a beautiful notification
def show_advanced_notification(title, msg, link=None):
    toast = Notification(
        app_id="Agent Aura",
        title=title,
        msg=msg,
        icon=ICON_PATH if os.path.exists(ICON_PATH) else "C:/Windows/System32/shell32.dll",
        duration="long"  # Longer notification
    )
    if link:
        toast.add_actions(label="Open Link", launch=link)
    
    # Set a custom audio (choose Default, Reminder, SMS, IM, Mail, Alarm2, etc.)
    toast.set_audio(audio.Reminder, loop=False)
    toast.show()

# Function to search Google for a topic using SerpApi
def fetch_alerts(query):
    try:
        search_url = f"https://serpapi.com/search?q={query.replace(' ', '+')}&api_key={SERP_API_KEY}"
        response = requests.get(search_url)

        if response.status_code == 200:
            results = response.json()
            result_links = []

            # Extract the top organic search results
            for result in results.get("organic_results", []):
                link = result.get("link")
                if link:
                    result_links.append(link)
            
            return result_links if result_links else None
        else:
            print("Failed to fetch search results from SerpApi.")
            return None
    except Exception as e:
        print(f"Error fetching search results: {e}")
        return None

# Function to monitor the alerts
def monitor_alerts(keywords):
    for topic in keywords:
        print(f"🔎 Searching for: {topic}")
        results = fetch_alerts(topic)
        if results:
            show_advanced_notification(
                title=f"🔔 {topic.title()} Found!",
                msg=f"Click below to check more about {topic}.",
                link=results[0]  # Show the first good result
            )
        else:
            show_advanced_notification(
                title=f"❗ No Results for {topic.title()}",
                msg="Try different keywords next time!",
                link=None
            )

# Function to actively search the internet for new updates
def search_and_alert():
    print("🔄 Checking for new content across the internet...")
    monitor_alerts(KEYWORDS_TO_SEARCH)

# Start by monitoring the internet with default keywords
search_and_alert()  # First manual input

# Set up periodic checks
schedule.every(NOTIFY_INTERVAL_MINUTES).minutes.do(search_and_alert)

# Run the scheduler for continuous checks
while True:
    schedule.run_pending()
    time.sleep(1)
