## Step 1: Import Libraries

import tkinter as tk
from tkinter import *
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import requests
import openai
import os
import time
import pyautogui
import smtplib
import pywhatkit as kit


## Step 2: Initialize Text-to-Speech (TTS)

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()


## Step 3: Listen to Microphone Input

# Function to capture voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except Exception as e:
            print("Couldn't understand...")
            return None


## Step 3: Replace GPT-4 with Local Ollama AI (Mistral/Gemma)
def chat_with_gpt(prompt):
    url = "http://localhost:11434/api/chat"  # Ollama local API endpoint
    payload = {
        "model": "mistral",  # Change to "gemma" or other if needed
        "messages": [
            {"role": "system", "content": "You are an AI assistant named Sweety."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, json=payload)
        response_json = response.json()
        return response_json['message']['content']
    except:
        return "I'm unable to connect to the AI model. Please make sure Ollama is running."

## Step 5: Open Websites and Play Songs

def play_song(song_name):
    search_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
    webbrowser.open(search_url)
    speak(f"Searching for {song_name} on YouTube")

def open_website(command):
    if "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif "google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif "notepad" in command:
        os.system("notepad")
        speak("Opening Notepad")


## Step 6: Control Your PC

def control_pc(command):
    if "volume up" in command:
        for i in range(5):
            pyautogui.press('volumeup')
        speak("Increasing volume")
    elif "volume down" in command:
        for i in range(5):
            pyautogui.press('volumedown')
        speak("Decreasing volume")
    elif "screenshot" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save(f"screenshot_{time.time()}.png")
        speak("Screenshot taken")
    elif "shutdown" in command:
        speak("Shutting down the computer")
        os.system("shutdown /s /t 5")
    elif "restart" in command:
        speak("Restarting the computer")
        os.system("shutdown /r /t 5")
    elif "log off" in command:
        speak("Logging off the computer")
        os.system("shutdown /l")


## Step 7: Get Weather Information

def get_weather():
    api_key = "YOUR_WEATHER_API_KEY"
    city = "Bangalore"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    speak(f"The current temperature in {city} is {temperature} degrees Celsius with {description}")


## Step 8: Send WhatsApp Message

def send_whatsapp():
    speak("Whom do you want to send the message to?")
    number = listen()
    speak("What message do you want to send?")
    message = listen()
    kit.sendwhatmsg_instantly(f"+91{number}", message)
    speak("Message sent successfully.")


## Step 9: Send Email

def send_email():
    speak("What should I write in the email?")
    content = listen()

    sender_email = "YOUR_EMAIL@gmail.com"
    sender_password = "YOUR_PASSWORD"
    receiver_email = "RECEIVER_EMAIL@gmail.com"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, content)
    server.close()
    speak("Email sent successfully.")


## Step 10: Build GUI for Sweety AI

def run_sweety():
    command = listen()
    if command:
        if "play" in command:
            song_name = command.replace("play", "").strip()
            play_song(song_name)
        elif "open" in command:
            open_website(command)
        elif "time" in command:
            time_now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time_now}")
        elif "weather" in command:
            get_weather()
        elif "send whatsapp" in command:
            send_whatsapp()
        elif "send email" in command:
            send_email()
        elif "volume up" in command or "volume down" in command or "screenshot" in command or "shutdown" in command or "restart" in command or "log off" in command:
            control_pc(command)
        elif "exit" in command or "bye" in command:
            speak("Goodbye! Have a nice day!")
            root.destroy()
        else:
            # New Feature: Anything not recognized will go to GPT-4
            gpt_response = chat_with_gpt(command)
            speak(gpt_response)


## Step 11: Setup GUI

root = Tk()
root.title("Sweety AI Assistant")
root.geometry("400x500")

label = Label(root, text="Sweety - AI Assistant", font=("Helvetica", 20))
label.pack(pady=20)

button = Button(root, text="Talk to Sweety", command=run_sweety)
button.pack(pady=10)

root.mainloop()
