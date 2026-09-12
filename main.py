import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os

recognizer = sr.Recognizer()

def speak(text):
    print("Assistant:", text)
    local_engine = pyttsx3.init()
    local_engine.say(text)
    local_engine.runAndWait()
    local_engine.stop()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error, please check your internet.")
        return ""

def listen_with_retry(max_attempts=2):
    for _ in range(max_attempts):
        command = listen()
        if command:
            return command
        speak("Please say that again.")
    speak("Going back to standby.")
    return ""

# def process_command(command):
#     if "time" in command:
#         now = datetime.datetime.now().strftime("%I:%M %p")
#         speak(f"The time is {now}")

#     elif "date" in command:
#         today = datetime.datetime.now().strftime("%B %d, %Y")
#         speak(f"Today is {today}")

#     elif "open google" in command:
#         speak("Opening Google")
#         webbrowser.open("https://google.com")

#     elif "open youtube" in command:
#         speak("Opening YouTube")
#         webbrowser.open("https://youtube.com")

#     elif "search wikipedia" in command:
#         speak("What should I search for?")
#         query = listen()
#         try:
#             result = wikipedia.summary(query, sentences=2)
#             speak(result)
#         except Exception:
#             speak("Couldn't find that on Wikipedia.")

#     elif "open notepad" in command:
#         speak("Opening Notepad")
#         os.startfile("notepad.exe")   # Windows only

#     elif "open calculator" in command:
#         speak("Opening Calculator")
#         os.startfile("calc.exe")      # Windows only

#     elif "tell me a joke" in command:
#         import pyjokes
#         speak(pyjokes.get_joke())

#     elif "stop" in command or "exit" in command:
#         speak("Goodbye!")
#         return False

#     else:
#         speak("Sorry, I don't know that command yet.")

#     return True

def cmd_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def cmd_date():
    today = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today is {today}")

def cmd_google():
    speak("Opening Google")
    webbrowser.open("https://google.com")

def cmd_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://youtube.com")

def cmd_wikipedia():
    speak("What should I search for?")
    query = listen()
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except Exception:
        speak("Couldn't find that on Wikipedia.")

def cmd_notepad():
    speak("Opening Notepad")
    os.startfile("notepad.exe")

def cmd_calculator():
    speak("Opening Calculator")
    os.startfile("calc.exe")

def cmd_joke():
    import pyjokes
    speak(pyjokes.get_joke())

def cmd_exit():
    speak("Goodbye!")
    return False

COMMANDS = {
    "time": cmd_time,
    "date": cmd_date,
    "open google": cmd_google,
    "open youtube": cmd_youtube,
    "search wikipedia": cmd_wikipedia,
    "open notepad": cmd_notepad,
    "open calculator": cmd_calculator,
    "tell me a joke": cmd_joke,
    "stop": cmd_exit,
    "exit": cmd_exit,
}

def process_command(command):
    for keyword, action in COMMANDS.items():
        if keyword in command:
            result = action()
            return result if result is not None else True
    speak("Sorry, I don't know that command yet.")
    return True

def wake_word_listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Waiting for wake word...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text.lower()
    except (sr.UnknownValueError, sr.RequestError):
        return ""

# Main loop
def main():
    speak("Assistant is on standby. Say the wake word to start.")
    running = True
    while running:
        trigger = wake_word_listen()
        if "hey assistant" in trigger or "hello assistant" in trigger:
            speak("Yes? How can I help?")
            command = listen_with_retry()
            if command:
                running = process_command(command)

if __name__ == "__main__":
    main()
