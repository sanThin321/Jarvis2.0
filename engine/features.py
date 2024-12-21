import sqlite3
import webbrowser
from playsound import playsound 
import eel
import os
from engine.config import ASSITANT_NAME
from engine.command import *
import pywhatkit as kit
import re
con=sqlite3.connect("jarvis.db")
cursor=con.cursor()


# Playing assistant sound function
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query=query.replace(ASSITANT_NAME,"")
    query=query.replace("open","")
    query.lower()

    # if query!="":
    #     speak("Opening "+query)
    #     os.system("start "+query)
    # else:
    #     speak("not found")
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

    

def PlayYoutube(query):
    search_term=extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def extract_yt_term(command):
    #define a regular expression pattern to capture the song name
    pattern=r'play\s+(.*?)\s+on\s+youtube'
    #use re.search to find the match in the command
    match=re.search(pattern,command,re.IGNORECASE)
    #if a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None 
