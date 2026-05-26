import speech_recognition as sr
import mysql.connector as sql
from collections import deque

def bfs_search(word_list, target):
    queue = deque([word_list[0]]) if word_list else deque()
    visited = set()
    while queue:
        current_word = queue.popleft()
        if current_word == target:
            return True 
        visited.add(current_word)
        for word in word_list:
            if word not in visited:
                queue.append(word)
    return False  
def save_to_database(text, conn):
    try:
        cursor = conn.cursor()
        sql1 = "INSERT INTO speec_text (speech) VALUES (%s)"
        cursor.execute(sql1, (text,))
        conn.commit()
        print("Speech text saved to the database")
    except sql.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        cursor.close()
try:
    conn = sql.connect(host='localhost', user='root', passwd='rohan@2006', database='speech')
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=1) 
        audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio)
    word_list = text.split()
    example=input("Enter the searching word:")
    print('\n')
    target_word = example  


    if bfs_search(word_list, target_word):
        print(f'Target word "{target_word}" found in speech text!')
        print("You said:", text)
        save_to_database(text, conn)
    else:
        print(f'Target word "{target_word}" not found.')
        print("You said:", text)
    
except sr.UnknownValueError:
    print("Sorry, could not understand the audio")
except sr.RequestError:
    print("Could not request results, please check your internet connection")
except sql.Error as e:
    print(f"Database error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
