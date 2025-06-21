import csv
import sqlite3
import datetime

con = sqlite3.connect("aura.db")
cursor = con.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
# cursor.execute(query)
# con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
# cursor.execute(query)
# con.commit()


# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# # Specify the column indices you want to import (0-based index)
# # Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 20]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
# con.close()

# query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890', 'null')"
# cursor.execute(query)
# con.commit()

# query = 'kunal'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])

#remainder db

# query = "CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY AUTOINCREMENT,task TEXT,time TEXT,repeat TEXT)"
# cursor.execute(query)


# query = "CREATE TABLE IF NOT EXISTS emotion_logs (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT,emotion TEXT,confidence REAL,timestamp TEXT)"
# cursor.execute(query)

# query = "CREATE TABLE IF NOT EXISTS session (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT,is_logged_in INTEGER)"
# cursor.execute(query)


def get_logged_in_user():
    try:
        con = sqlite3.connect(con)
        cursor = con.cursor()
        cursor.execute("SELECT email FROM session WHERE is_logged_in = 1 ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        con.close()
        return row[0] if row else None
    except Exception as e:
        print(f"[DB ERROR] get_logged_in_user: {e}")
        return None

def save_emotion_to_db(email, emotion, confidence):
    try:
        con = sqlite3.connect(con)
        cursor = con.cursor()
        cursor.execute('''
            INSERT INTO emotion_logs (email, emotion, confidence, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (email, emotion, confidence, datetime.now().isoformat()))
        con.commit()
        con.close()
    except Exception as e:
        print(f"[DB ERROR] save_emotion_to_db: {e}")


# query = "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id TEXT,key TEXT,value TEXT)"
# cursor.execute(query)



