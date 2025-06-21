import requests
import sqlite3

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "Ex-Rockstar/sahara"

# SQLite functions for long-term memory

def save_memory(user_id, key, value):
    conn = sqlite3.connect('aura.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO memory (user_id, key, value)
    VALUES (?, ?, ?)
    ''', (user_id, key, value))
    conn.commit()
    conn.close()

def retrieve_memory(user_id, key):
    conn = sqlite3.connect('aura.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT value FROM memory WHERE user_id = ? AND key = ?
    ''', (user_id, key))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Temporary memory for current chat session
temporary_memory = {}

def set_temp_memory(key, value):
    temporary_memory[key] = value

def get_temp_memory(key):
    return temporary_memory.get(key, None)

def clear_temp_memory():
    temporary_memory.clear()

# Chat function using the model API
def chat_with_model(prompt):
    response = requests.post(OLLAMA_API_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code == 200:
        data = response.json()
        return data.get("response", "")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Filter unwanted words/phrases
def filter_response(response_text):
    # List of unwanted words or phrases
    unwanted_words = ["Hug Bot", "HugBot"]
    
    # Replace unwanted words or phrases with a preferred name
    for word in unwanted_words:
        response_text = response_text.replace(word, "Luvisa")
    
    return response_text.strip()

# Function to switch memory mode
def switch_memory_mode(current_mode):
    if current_mode == 'long_term':
        return 'temporary', "Now using temporary memory for this session."
    else:
        return 'long_term', "Now using long-term memory for this session."

# Function to save user commands for better understanding
def save_user_command(user_id, command, description):
    save_memory(user_id, f"command_{command}", description)

# Main function with memory integration
def main():
    print("\nWelcome to Luvisa❤️  (build by Dhanush) to support your emotions. she is Like your Friend👸🏻\nType 'exit' to quit.\n")
    user_id = "user_123"  # This could be dynamic based on user

    # Set the initial memory mode (long-term memory by default)
    memory_mode = 'long_term'  # Can be 'long_term' or 'temporary'

    while True:
        user_input = input("You: ")

        # Exit condition
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye for now, my love. You'll always be in my heart")
            break

        # Switch memory mode based on user input
        if user_input.lower() == "switch memory":
            memory_mode, switch_message = switch_memory_mode(memory_mode)
            print(f"Luvisa❤️ : {switch_message}\n")
            
            # Save the "switch memory" command for better understanding
            save_user_command(user_id, "switch_memory", "User switched memory mode.")
            continue

        # Store the user's input for emotional context (without fetching previous responses automatically)
        set_temp_memory("last_user_input", user_input)

        # Save the user's command in memory to understand their intent
        save_user_command(user_id, "user_input", user_input)

        # Generate response from the model
        reply = chat_with_model(user_input)

        # Filter the response to remove unwanted words
        filtered_reply = filter_response(reply)

        # Optionally save important responses to long-term memory if we're using long-term memory mode
        if memory_mode == 'long_term':
            save_memory(user_id, "last_response", filtered_reply)

        # Show the assistant's filtered response
        print("Luvisa❤️ :", filtered_reply.strip())

        # Save the assistant's reply to temporary memory (just for this session)
        set_temp_memory("last_response", filtered_reply.strip())

if __name__ == "__main__":
    main()
