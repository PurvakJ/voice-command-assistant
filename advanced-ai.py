import requests
import wikipedia
import warnings
import wolframalpha
import yfinance as yf
from translate import Translator
import random
import re
import webbrowser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import geocoder
import subprocess
from instabot import Bot
import pywhatkit
import pyautogui
import imageio
import keyboard
import time
from plyer import notification
import datetime
from datetime import datetime, timedelta
import speech_recognition as sr
import pyttsx3
import threading
import cv2
from pynput.keyboard import Key, Controller
from time import sleep


# Load the pre-trained Haarcascades face classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
counting = 0
count = 0

def speech():
    recognizer = sr.Recognizer()
    count = 0

    while True:
        with sr.Microphone() as source:
            print("Listening Sir......")
            speak("Listening sir")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=10)

        try:
            # The audio has already been captured in the previous block
            output = recognizer.recognize_google(audio)
            print("You said:", output)
            return output  # Return the output variable when successful
        except sr.UnknownValueError:
            count += 1
            print("Could not understand audio")
            speak("Could not understand audio")
            if count == 3:
                print("Sorry Sir, can you type your Command")
                speak("Sorry sir, can you type your command")
                output = input("Enter your Command Sir: ")
                count = 0
                speak(output)
                return output  # Return the output variable when the user types a command
            continue
        except sr.RequestError as e:
            print(f"Error with the API request; {e}")
            speak("An error occurred")
            continue
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            speak("Listening timed out. Please try again")
            continue

def speak(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 180)  # Speed of speech

    # Use the engine to speak the provided text
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()


api_key = "d1845658f92b31c64bd94f06f7188c9c"
reminder_states = {}

def record_screen():
    screen_size = (1920, 1080)
    output_filename = 'screen_record.mp4'
    output_text = "Screen Recording is on"
    speak(output_text)
    print("Press 'q' to exit")

    fps = 30
    writer = imageio.get_writer(output_filename, fps=fps)

    try:
        while True:
            screenshot = pyautogui.screenshot()
            frame = imageio.core.asarray(screenshot)
            writer.append_data(frame)
            output = speech()
            valid_output = ["quit", "exit", "return", "close", "stop"]
            output = next((valid for valid in valid_output if output in output.lower()), None)
            if output in ["quit", "exit", "return", "close", "stop"]:
                pyautogui.hotkey('q')
                if keyboard.is_pressed('q'):
                    raise KeyboardInterrupt

    except KeyboardInterrupt:
        writer.close()
        print("Screen recording stopped. Video saved as", output_filename)
        output_text = "Screen recording stopped"
        speak(output_text)

def record_audio():
    pyautogui.press("super")
    pyautogui.sleep(5)
    pyautogui.typewrite("voice recorder")
    pyautogui.press("enter")
    pyautogui.sleep(2)
    speak("voice recording is launching sir")
    pyautogui.press("enter")

    want = "when you want to stop the recording ask stop or close or exit"
    print(want)
    speak(want)
    output = speech()
    valid_output = ["quit", "exit", "return", "close", "stop"]
    output = next((valid for valid in valid_output if output in output.lower()), None)
    if output in ["quit", "exit", "return", "close", "stop"]:
        pyautogui.press("enter")
        want = "recording complete sir"
        print(want)
        speak(want)
    pyautogui.hotkey('ctrl','w')



def send_whatsapp_message():
    current_time = datetime.datetime.now().time()
    output = "Enter the message to be sent: "
    print(output)
    speak(output)
    message = speech()
    output = "Enter the number of the receiver: "
    print(output)
    speak(output)
    user = speech()
    recipient_number = (f"+91{user}")
    hours, minutes = current_time.hour, current_time.minute
    pywhatkit.sendwhatmsg(recipient_number, message, hours, minutes + 2)
    pyautogui.hotkey('enter')
    text = "Message sent"
    print(text)
    speak(text)

def instabot_actions():
    my_bot = Bot()
    my_bot.login(username="purvak_jindal", password="011021")
    output = "What do you want to got from instabot: "
    print(output)
    speak(output)
    query = speech()
    valid_websites = ["unfollow", "follow", "upload", "send message", "send msg", "message", "msg", "story", "upload story", "upload_story", "like", "like user", "comment", "following_list", "followers_list", "following", "followers"]

    matched_website = next((site for site in valid_websites if site in query.lower()), None)
    output = f"Opening {matched_website} sir..."
    print(output)
    speak(output)

    if matched_website == "unfollow":
        unfollow = "Enter the username you want to unfollow"
        print(unfollow)
        speak(unfollow)
        unfollow = speech()
        my_bot.unfollow(unfollow)
        done = "Done sir"
        print(done)
        speak(done)
    if matched_website == "unfollow":
        follow = "Enter the username you want to follow"
        print(follow)
        speak(follow)
        follow = speech()
        my_bot.follow(follow)
        done = "Done sir"
        print(done)
        speak(done)
    # if matched_website == "upload":
    #     my_bot.upload_photo("mine.jpg", caption="yes this is me")
    #     my_bot.upload_video()
    #     done = print("Done sir")
    #     speak(done)
    # if matched_website == "upload story" or "story":
    #     my_bot.upload_story_photo()
    #     done = print("Done sir")
    #     speak(done)
    if matched_website in ["message", "msg", "send message", "send msg"]:
        message = "Enter the message you want to: "
        print(message)
        speak(message)
        message = speech()
        user_id = "Enter the user id"
        print(user_id)
        speak(user_id)
        user_id = speech()
        my_bot.send_message(message, user_id)
        done = "Done sir"
        print(done)
        speak(done)
    # if matched_website == "like":
    #     user = "Enter the user id"
    #     print(user)
    #     speak(user)
    #     user = speech()
    #     my_bot.like_user("", amount=2, filtration=False)
    #     user = my_bot.get_user_id_from_username("")
    #     media_id = my_bot.get_last_user_medias(user, 1)
    #     done = "Done sir"
    #     print(done)
    #     speak(done)
    # if matched_website == "comment":
    #     comment = "enter the comment"
    #     print(comment)
    #     speak(comment)
    #     comment = speech()
    #     my_bot.comment(media_id[0], comment)
    #     done = "Done sir"
    #     print(done)
    #     speak(done)
    if matched_website == "following":
        user = "Enter the user id"
        print(user)
        speak(user)
        user = speech()
        following_list = my_bot.get_user_following(user)
        print(following_list)
        speak(following_list)
        done = "Done sir"
        print(done)
        speak(done)
    if matched_website == "followers":
        user = "Enter the user id"
        print(user)
        speak(user)
        user = speech()
        followers_list = my_bot.get_user_followers(user)
        print(followers_list)
        speak(followers_list)
        done = "Done sir"
        print(done)
        speak(done)

def open_camera():

        yes = "Do you want to click the pic or video? "
        print(yes)
        speak(yes)
        output = speech()
        valid_output = ["picture", "video", "camera", "photo"]
        yes = next((valid for valid in valid_output if output in output.lower()), None)
        if yes in ["picture", "camera", "photo"]:
            pyautogui.press("super")
            pyautogui.sleep(5)
            pyautogui.typewrite("camera")
            pyautogui.sleep(5)
            pyautogui.press("enter")
            pyautogui.sleep(2)
            speak("SMILE")
            pyautogui.sleep(5)
            pyautogui.press("enter")
            photo = "photo captured"
            speak(photo)

    # Ask if the user wants to play a video
        elif yes == "video":
            pyautogui.press("super")
            pyautogui.sleep(5)
            pyautogui.typewrite("camera")
            pyautogui.sleep(5)
            pyautogui.press("enter")
            pyautogui.sleep(2)
            speak("SMILE")
            pyautogui.press('up')
            pyautogui.sleep(5)
            pyautogui.press("enter")
            video = "video capturing"
            speak(video)
            want = "When you want to stop recording ask stop or exit"
            print(want)
            speak(want)
            output = speech()
            valid_output = ["quit", "exit", "return", "close", "stop"]
            output = next((valid for valid in valid_output if output in output.lower()), None)
            if output in ["quit", "exit", "return", "close", "stop"]:
                pyautogui.press("enter")
            video = "video captured sir"
            print(video)
            speak(video)
            pyautogui.press('down')

        pyautogui.hotkey('ctrl', 'w')

def open_microsoft_office(choice):
    Ms = choice
    valid_ms = ["word", "excel", "powerpoint", "msaccess", "access", "ms access", "notepad", "power point", "cmd", "command prompt"]
    matched_ms = next((valid for valid in valid_ms if valid in Ms.lower()), None)

    if matched_ms == "word":
        print("Opening Microsoft Word...")
        speak("Opening Microsoft word")
        subprocess.run(["start", "winword.exe"], shell=True)
    elif matched_ms == "excel":
        print("Opening Microsoft Excel...")
        speak("Opening Microsoft excel")
        subprocess.run(["start", "excel.exe"], shell=True)
    elif matched_ms == "powerpoint" or matched_ms == "power point":
        print("Opening Microsoft PowerPoint...")
        speak("opening powerpoint")
        subprocess.run(["start", "POWERPNT.EXE"], shell=True)
    elif matched_ms == "notepad":
        print("Opening Microsoft Notepad...")
        speak("openign notepad")
        subprocess.run(["start", "notepad.EXE"], shell=True)
    elif matched_ms == "ms access" or matched_ms == "msaccess" or matched_ms == "access":
        print("Opening Microsoft MS Access...")
        speak("opening ms access")
        subprocess.run(["start", "msaccess.EXE"], shell=True)
    elif matched_ms == "cmd" or matched_ms == "command prompt":
        print("opening Command Prompt...")
        speak("opening command prompt")
        subprocess.run("cmd.exe")
    else:
        print("Sorry, we cannot access this application right now.")
        speak("Sorry, we cannot access this application right now")


def get_current_location():
    try:
        location = geocoder.ip('me')
        speak(location)
        return location
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("an error occured")
        return None


def send_email(subject, body, to_email, smtp_server, smtp_port, sender_email, sender_password):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
        print("Email sent successfully!")
        speak("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        speak("An error occured")


def search_file():
    output = "Want to enter the file manually or by speech"
    print(output)
    speak(output)
    ms = output
    valid_ms = ["manually", "speach", "type", "typing", "talk", "ask"]
    file_to_search = next((valid for valid in valid_ms if valid in ms.lower()), None)

    if file_to_search in ["manually", "type", "typing"]:
        file_to_search = input("Enter the file name to search for: ")
        speak(f"Searching for {file_to_search}")
        root_dirs = ["D:\\", "C:\\"]
        found = False
    else:
        file_to_search = speech()
        speak(f"Searching for {file_to_search}")
        root_dirs = ["D:\\", "C:\\"]
        found = False

    for root_dir in root_dirs:
        for rel_path, dirs, files in os.walk(root_dir):
            if file_to_search in files:
                full_path = os.path.join(rel_path, file_to_search)
                output = f"File found: {full_path}"
                print(output)
                speak(output)
                os.startfile(full_path)
                found = True
                break

    if not found:
        print(f"No matching file found for '{file_to_search}' in the specified directories.")
        speak("No matching found in your directories")


def open_website(choice):
    query = choice
    valid_websites = ["wikipedia", "google", "facebook", "instagram", "chatgpt", "telegram", "snapchat",
                      "telegrambot", "youtube", "whatsapp", "gmail", "flipkart", "amazon", "hotstar", "amazonprime",
                      "netflix", "zee5", "map", "googlemap", "google map"]

    matched_website = next((site for site in valid_websites if site in query.lower()), None)
    if matched_website == "youtube":
        want = "what you want to watch on youtube"
        print(want)
        speak(want)
        want = speech()
        webbrowser.open(f"https://www.youtube.com/results?search_query={want}")

    output = f"Opening {matched_website} sir..."

    print(output)
    speak(output)
    if matched_website == "whatsapp":
        webbrowser.open("https://web.whatsapp.com/")
    elif matched_website == "map" or matched_website == "googlemap" or matched_website == "google map":
        webbrowser.open("https://www.google.com/maps")
    elif matched_website:
        webbrowser.open(f"https://www.{matched_website}.com")
    else:
        print("Invalid website name or not be in our file directory.")
        speak("Invalid website name or not be in out file directory")


def get_response():
    R_EATING = "I don't like eating anything because I'm a bot obviously!"
    R_ADVICE = "If I were you, I would go to the internet and type exactly what you wrote there!"

    # Additional responses for end questions
    R_END_QUESTION = "I'm just a bot, so I don't have personal experiences. What else would you like to know?"
    R_GOODBYE = "Goodbye! If you have more questions, feel free to ask."

    # Define responses and associated word lists in a dictionary
    RESPONSES = {
        'Hello!': ['hello', 'hi', 'hey', 'sup', 'heyo'],
        'See you!': ['bye', 'goodbye'],
        'I\'m doing fine, and you?': ['how', 'are', 'you', 'doing'],
        'You\'re welcome!': ['thank', 'thanks'],
        'Thank you!': ['i', 'love', 'code', 'palace'],
        R_ADVICE: ['give', 'advice'],
        R_EATING: ['what', 'you', 'eat'],
        R_END_QUESTION: ['what', 'else', 'you', 'know'],
        R_GOODBYE: ['exit', 'bye', 'goodbye']
    }

    def unknown():
        return random.choice(
            ["Could you please re-phrase that? ", "...", "Sounds about right.", "What does that mean?"])

    def message_probability(user_message, recognized_words, single_response=False, required_words=set()):
        message_certainty = sum(word in recognized_words for word in user_message)
        percentage = message_certainty / len(recognized_words) if recognized_words else 0
        has_required_words = required_words.issubset(user_message)

        if has_required_words or single_response:
            return int(percentage * 100)
        else:
            return 0

    def check_all_messages(message):
        highest_prob_list = {}

        def response(bot_response, list_of_words, single_response=False, required_words=set()):
            highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response,
                                                                  required_words)

        for bot_response, word_list in RESPONSES.items():
            response(bot_response, word_list)

        best_match = max(highest_prob_list, key=highest_prob_list.get)
        return unknown() if highest_prob_list[best_match] < 1 else best_match

    def get_response(user_input):
        split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
        response = check_all_messages(split_message)
        return response

    # Testing the response system
    while True:
        user_input = input('You: ')
        if user_input.lower() in ['exit', 'bye', 'goodbye']:
            output = print('Bot:', R_GOODBYE)
            speak(output)
            break
        output = print('Bot:', get_response(user_input))
        speak(output)


def translate_text():
    text_to_translate = "Enter the text to translate: "
    print(text_to_translate)
    speak(text_to_translate)
    text_to_translate = speech()
    to_lang = "Enter the language for translation: "
    print(to_lang)
    speak(to_lang)
    to_lang = speech()
    translator = Translator(to_lang=to_lang)
    translated_text = translator.translate(text_to_translate)

    print(translated_text)
    speak(translated_text)


def get_joke():
    hindi_jokes_api = 'https://hindi-jokes-api.onrender.com/jokes?api_key=131aa693d309a20a8f51c7a33999'
    data = requests.get(hindi_jokes_api)
    data_json = data.json()
    output = data_json['jokeContent']
    print(output)
    speak(output)

def get_stock_data():
    def get_ticker_symbol(stock_name):
        # You can create a dictionary to map stock names to their respective ticker symbols
        stock_mapping = {
            stock_name.upper(): stock_name.upper() + '.NS'
            # Add more mappings as needed
        }

        # Check if the stock name exists in the mapping
        if stock_name.upper() in stock_mapping:
            return stock_mapping[stock_name.upper()]
        else:
            raise ValueError(f"Ticker symbol not found for stock: {stock_name}")

    # Example usage:
    stock_name_input = "Enter the stock name (e.g., RELIANCE, TCS): "
    print(stock_name_input)
    speak(stock_name_input)
    stock_name_input = speech()
    ticker_symbol = get_ticker_symbol(stock_name_input)
    end_point = datetime.now()
    end_date = end_point.strftime('%Y-%m-%d')
    # Get data for the specified ticker symbol
    ticker_data = yf.Ticker(ticker_symbol)
    ticker_df = ticker_data.history(period='1d', start='2024-01-01', end=end_date)

    # Display the historical prices
    print(ticker_df)


def get_news():
    news_api_key = '710e550e4c804d6b9a2c77f56c894105'
    news_url = "https://newsapi.org/v2/top-headlines?country=in&apikey=" + news_api_key
    news = requests.get(news_url).json()
    articles = news['articles']
    news_headlines = []

    for art in articles:
        news_headlines.append(art['title'])

    want = "How many top news you want to see"
    print(want)
    speak(want)
    news = speech()

    for i in range(min(news, len(news_headlines))):
        news_head = news_headlines[i]
        print(news_head)
        speak(news_head)


def wolframalpha_query():
    wolframalpha_api = 'W9XVYU-4YVL7RAPWY'
    client = wolframalpha.Client(wolframalpha_api)
    try:
        text = "Enter your question: "
        print(text)
        speak(text)
        text = speech()
        result = client.query(text)
        answer = next(result.results).text
        print(answer)
        speak(answer)
    except Exception as e:
        print(f'Data not found: {e}')
        speak("Data not found")


def set_reminder():

    def get_user_input():
        title = "Enter the title of the notification: "
        print(title)
        speak(title)
        title = speech()
        message = "Enter the message of the notification: "
        print(message)
        speak(message)
        message = speech()
        timeout_str = "In how much time you need your reminder in HH format: "
        print(timeout_str)
        speak(timeout_str)
        timeout_str = speech()
        timeout_strr = "In how much time you need your reminder in MM format: "
        print(timeout_strr)
        speak(timeout_strr)
        timeout_strr = speech()
        return title, message, timeout_str, timeout_strr

    def get_timeout(timeout_str, timeout_strr):
        try:
            hours, minutes = timeout_str, timeout_strr
            timeout = datetime.timedelta(hours=hours, minutes=minutes)
            return timeout
        except ValueError:
            print("Invalid input for timeout. Please enter in HH:MM format.")
            speak("Invalid input for timeout. Please enter in HH:MM format")
            exit()

    def display_notification(title, message):
        notification.notify(
            title="ALERT: " + title,
            message=f"{message}\nTime: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            timeout=10
        )

    title, message, timeout_str = get_user_input()
    timeout = get_timeout(timeout_str)

    current_time = datetime.datetime.now()
    reminder_time = current_time + timeout

    output = f"Reminder set for: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}"
    print(output)
    speak(output)

    while True:
        current_time = datetime.now()

        if current_time >= reminder_time and title not in reminder_states:
            display_notification(title, message)
            reminder_states[title] = True
            break
        time.sleep(1)

def get_current_date_time():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    output = "Present Date and Time:", formatted_datetime
    print(output)
    speak(output)


def wikipedia_search():
    warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")
    topic = "Enter the topic you want to search on Wikipedia: "
    print(topic)
    speak(topic)
    topic = speech()

    try:
        answer = "Do you want full knowledge or only basic knowledge? (y/n): "
        print(answer)
        speak(answer)
        answer = speech()
        if answer.lower() == 'y':
            print(wikipedia.page(topic).content)
            speak(wikipedia.page(topic).content)
        else:
            print(wikipedia.summary(topic))
            speak(wikipedia.summary(topic))
        output = "Is you want to open wikipedia website"
        print(output)
        speak(output)
        query = speech()
        valid_websites = ["yes", "okay", "open"]

        matched_website = next((site for site in valid_websites if site in query.lower()), None)
        if matched_website in ["yes", "okay", "open"]:
            output = "Opening wikipedia sir..."
            print(output)
            speak(output)
            webbrowser.open("https://web.wikipedia.com/")
        else:
            return

    except wikipedia.exceptions.PageError:
        print("Page not found.")
        speak("Page not found")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        speak("Error Occurred")


def get_and_display_weather():
    api_key = "d1845658f92b31c64bd94f06f7188c9c"
    city = get_current_location()
    print(city)
    speak(city)
    city = speech()
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        if weather_data:
            output = print(f"Weather in {weather_data['name']}, {weather_data['sys']['country']}:")
            speak(output)
            output = print(f"Temperature: {weather_data['main']['temp']}°C")
            speak(output)
            output = print(f"Description: {weather_data['weather'][0]['description']}")
            speak(output)
            output = print(f"Humidity: {weather_data['main']['humidity']}%")
            speak(output)
            output = print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
            speak(output)
        else:
            print("Failed to fetch weather data.")
            speak("Failed to fetch weather data")
    else:
        print(f"Error {response.status_code}: {response.text}")
        speak("An error occurred")
        return None

# API key for OpenWeatherMap. Replace with your own key.
def write_text(choice):
    want = choice
    valid_choice = ["text", "type", "write", "copy", "paste", "select", "typing", "enter", "escape", "delete", "backspace"]
    want = next((valid for valid in valid_choice if valid in want.lower()), None)
    if want in ["type", "typing", "text"]:
        text = "enter the text you want to enter"
        speak(text)
        text = speech()
        speak(text)
        pyautogui.typewrite(text, interval=0.1)
    elif want == "copy":
        pyautogui.hotkey('ctrl', 'c')
    elif want == "paste":
        pyautogui.hotkey('ctrl', 'v')
    elif want == "select":
        pyautogui.hotkey('ctrl', 'a')
    elif want == "enter":
        pyautogui.press('enter')
    elif want == "escape":
        pyautogui.press('esc')
    elif want == "tab":
        pyautogui.press('tab')
    elif want in ["capslock", "capslock"]:
        pyautogui.press('capslock')
    elif want == "space":
        pyautogui.press('space')
    elif want == "delete":
        pyautogui.press('delete')
    elif want == "backspace":
        pyautogui.press('backspace')

def alarm():
    hours = "Enter the time in hours: "
    print(hours)
    speak(hours)
    hours = int(speech())
    min = "Enter the time in minutes: "
    print(min)
    speak(min)
    min = int(speech())
    # Set seconds to 00
    seconds = 0

    # Create the alarm time object
    alarm_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, hours, min, seconds)

    # Main loop
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")

        # Check if it's time for the alarm
        if current_time == alarm_time.strftime("%H:%M:%S"):
            print("Alarm ringing, sir")
            speak("alarm ringing, sir")
            os.startfile("D:/downloads/alarm.mp3")  # Replace with your alarm sound
            break  # Exit the loop after the alarm is triggered

        # Optional: Add a delay to avoid high CPU usage
        # You can adjust the sleep duration based on your needs
        time.sleep(1)


def controler(choice):
    keyboard = Controller()
    control = choice
    valid_cn = ["pause", "stop", "play", "replay", "mute", "unmute", "increase", "decrease", "up", "down"]
    control = next((valid for valid in valid_cn if valid in control.lower()), None)

    if control == "pause" or control == "stop":
        pyautogui.press("space")
        speak("video paused")
    elif control == "play" or control == "replay":
        pyautogui.press("space")
        speak("video played")
    elif control == "mute":
        pyautogui.press("m")
        speak("video muted")
    elif control == "unmute":
        pyautogui.press("m")
        speak("video muted")
    elif control == "increase" or control == "up":
        value = "How much volume you want to increase"
        print(value)
        speak(value)
        value = speech()
        value = value.lower()
        if value == "one":
            value = 1
        elif value == "two":
            value = 2
        elif value == "three":
            value = 3
        elif value == "four":
            value = 4
        elif value == "five":
            value = 5
        elif value == "six":
            value = 6
        elif value == "seven":
            value = 7
        elif value == "eight":
            value = 8
        elif value == "nine":
            value = 9
        elif value == "ten":
            value = 10
        else: 
            return value
        from keyboard import volumeup
        speak("Turning volume up,sir")
        for i in range(int(value)):
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
            sleep(0.1)
    elif control == "decrease" or control == "down":
        value = "How much volume you want to decrease"
        print(value)
        speak(value)
        value = speech()
        value = value.lower()
        if value == "one":
            value = 1
        elif value == "two":
            value = 2
        elif value == "three":
            value = 3
        elif value == "four":
            value = 4
        elif value == "five":
            value = 5
        elif value == "six":
            value = 6
        elif value == "seven":
            value = 7
        elif value == "eight":
            value = 8
        elif value == "nine":
            value = 9
        elif value == "ten":
            value = 10
        else:
            return value
        from keyboard import volumedown
        speak("Turning volume down,sir")
        for i in range(int(value)):
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
            sleep(0.1)


def main():
    result = run_face_detection()

    # If face authentication is successful, proceed to other functions
    if result:
        hour = int(datetime.now().hour)
        if hour >= 0 and hour <= 12:
            speak("Good Morning,sir")
        elif hour > 12 and hour <= 18:
            speak("Good Afternoon ,sir")

        else:
            speak("Good Evening,sir")

        print("Welcome back to your Assistant Program!")
        speak("Welcome back to your assistant program")
        speak("Please tell me, How can I help you ?")

        while True:
            choice = speech()

            valid_choice = ["screen record", "screen recording", "screen", "audio recording", "audio record", "audio",
                            "send message on whatsapp",
                            "whatsapp", "send the message on whatsapp", "send the message on instagram", "instagram",
                            "send message on instagram",
                            "video record", "video recording", "video", "pic", "picture", "camera", "word", "excel",
                            "powerpoint",
                            "power point", "msaccess", "ms access",
                            "notepad", "location", "email", "file", "search file", "searchfile", "search", "wikipedia",
                            "google",
                            "facebook", "instagram", "voice recording", "audiorecording", "voicerecording"
                            "chatgpt", "telegram", "snapchat", "telegrambot", "youtube", "whatsapp", "gmail",
                            "flipkart",
                            "amazon", "hotstar", "app"
                            "amazonprime", "amazon prime", "netflix", "zee5", "map", "googlemap", "google map",
                            "translate", "screenshot", "screen shot", "alarm",
                            "stock", "joke", "news", "cmd", "command prompt", "delete", "backspace"
                            "reminder", "notification", "date", "time", "wikipedia", "wiki", "wiki pedia", "weather",
                            "copy", "paste", "select", "write", "text", "typing", "tab", "caps lock", "capslock",
                            "type", "close", "bye", "exit", "goodbye", "good bye", "quit", "sleep", "rest",
                            "hello", "i am fine", "how are you", "thank you", "thanks", "close", "space", "shutdown",
                            "pause", "stop", "play", "replay", "mute", "unmute", "increase", "decrease", "up", "down"]
            choice = next((valid for valid in valid_choice if valid in choice.lower()), None)

            if choice in ["exit", "bye", "goodbye", "good bye", "quit", "sleep", "rest"]:
                print("Exiting the Assistant Program. Goodbye! Sir")
                speak("Exiting the Assistant program. goodbye sir")
                break
            elif choice == "hello":
                speak("Hello sir, how are you ?")
            elif choice == "i am fine":
                speak("that's great, sir")
            elif choice == "how are you":
                speak("Perfect, sir")
            elif choice in ["thank you", "thanks"]:
                speak("you are welcome, sir")
            elif choice == "screenrecord":
                record_screen()
            elif choice in ["audio", "audio recording", "audiorecording", "voice recording", "voicerecording", "audiorecording"]:
                record_audio()
            elif choice == "whatsapp":
                send_whatsapp_message()
            elif choice == "instagram":
                instabot_actions()
            elif choice in ["video", "camera", "pic", "picture"]:
                open_camera()
            elif choice in ["word", "excel", "powerpoint", "power point", "msaccess", "ms access", "notepad", "cmd", "command prompt"]:
                open_microsoft_office(choice)
            elif choice == "location":
                location = get_current_location()
                print("Current Location:", location)
            elif choice == "email":
                subject = input("Enter the Subject of the mail: ")
                speak(subject)
                body = input("Enter the Body of the mail: ")
                speak(body)
                to_email = input("Enter the Reciever email: " + "@gmail.com")
                speak(to_email)
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                sender_email = "purvakjindal2102@gmail.com"
                sender_password = "lprn stpl tocb wqbq"
                send_email(subject, body, to_email, smtp_server, smtp_port, sender_email, sender_password)
            elif choice in ["file", "search file", "searchfile", "search"]:
                search_file()
            elif choice in ["google", "facebook", "instagram", "chatgpt", "telegram", "snapchat", "telegrambot",
                            "youtube", "whatsapp", "gmail", "flipkart", "amazon", "hotstar", "amazonprime", "netflix",
                            "zee5", "map", "googlemap", "google map"]:
                open_website(choice)
            # elif choice == "11":
            #     get_response()
            elif choice == "translate":
                translate_text()
            elif choice == "joke":
                get_joke()
            elif choice == "stock":
                get_stock_data()
            elif choice == "news":
                get_news()
            elif choice in ["reminder", "notification"]:
                set_reminder()
            elif choice in ["date", "time"]:
                get_current_date_time()
            elif choice in ["wiki", "wikipedia", "wiki pedia"]:
                wikipedia_search()
            elif choice == "weather":
                get_and_display_weather()
            elif choice in ["type", "write", "copy", "paste", "select", "typing", "enter", "escape", "tab", "caps lock", "capslock", "space"]:
                write_text(choice)
            elif choice == "close":
                pyautogui.hotkey("ctrl", "w")
            elif choice == "shutdown":
                speak("Are You sure you want to shutdown")
                shutdown = "Do you wish to shutdown your computer? (yes/no)"
                speak(shutdown)
                shutdown = speech()
                if shutdown == "yes":
                    os.system("shutdown /s /t 1")

                elif shutdown == "no":
                    break
            elif choice in ["screenshot", "screen shot"]:
                im = pyautogui.screenshot()
                name = "Enter the name of photo to store"
                print(name)
                speak(name)
                name = speech()
                im.save(f"{name}.jpg")
            elif choice == "app":
                want = "Enter the only app name you want to open"
                print(want)
                speak(want)
                want = speech()
                pyautogui.press("super")
                pyautogui.sleep(5)
                pyautogui.press(want)
                pyautogui.press("enter")
            elif choice == "alarm":
                alarm()
            elif choice in ["pause", "stop", "play", "replay", "mute", "unmute", "increase", "decrease", "up", "down"]:
                controler(choice)
            else:
                wolframalpha_query()
    else:
        print("Authentication failed. Access denied.")

def run_face_detection():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    reference_img = cv2.imread("D:/downloads/mine.jpg", cv2.IMREAD_GRAYSCALE)

    def check_face(frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            if len(faces) > 0:
                x, y, w, h = faces[0]
                current_face = gray[y:y + h, x:x + w]
                reference_face = cv2.resize(reference_img, (w, h))

                # Dummy implementation - always consider it a match
                return True
            else:
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    while True:
        ret, frame = cap.read()
        if ret:
            if threading.active_count() < 2:
                result = check_face(frame.copy())
                threading.Thread(target=lambda: process_result(result)).start()

            if check_face(frame):
                cap.release()
                cv2.destroyAllWindows()
                return True
            else:
                print("Authentication error!!!")
                global counting
                counting += 1
                time.sleep(2)
                if counting == 10:
                    print("You do not have access to operate the AI.")
                    return False

            cv2.imshow("video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    return False

def process_result(result):
    if result:
        print("Authentication successful!")
    else:
        print("Authentication failed.")


if __name__ == "__main__":
    main()
