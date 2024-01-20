import requests
from requests import request, session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import wikipedia
import warnings
import wolframalpha
import yfinance as yf
import pandas as pd
from translate import Translator
from openai import OpenAI
import random
import re
import webbrowser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import geocoder
import sys
import pygame
import subprocess
from instabot import Bot
import pywhatkit
import sounddevice as sd
import wavio
import pyautogui
import imageio
import keyboard
import time
from plyer import notification
import datetime
from datetime import datetime
import speech_recognition as sr
import pyttsx3

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
            output = recognizer.recognize_google(audio)
            output = output.lower()
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
                return output  # Return the output variable when user types command
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
            valid_output = ["quit", "exit", "return", "close"]
            output = next((valid for valid in valid_output if output in output.lower()), None)
            if output in ["quit", "exit", "return", "close"]:
                pyautogui.hotkey('q')
                if keyboard.is_pressed('q'):
                    raise KeyboardInterrupt

    except KeyboardInterrupt:
        writer.close()
        print("Screen recording stopped. Video saved as", output_filename)
        output_text = "Screen recording stopped"
        speak(output_text)

def record_audio(duration=None, sample_rate=44100, filename="output.wav"):
    if duration is None:
        duration = float(input("Enter the duration of the voice record you want: "))
        speak(duration)

    output_text = "Recording..."
    print(output_text)
    speak(output_text)

    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()

    output_text = "Recording complete."
    print(output_text)
    speak(output_text)

    wavio.write(filename, audio_data, sample_rate, sampwidth=3)

    print(f"Audio saved as {filename}")


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
    pygame.init()

    pygame.camera.init()

    # List available cameras
    camera_list = pygame.camera.list_cameras()

    if not camera_list:
        camera = "No cameras found."
        print(camera)
        speak(camera)
        pygame.quit()
        exit()

    # Use the first available camera
    camera = pygame.camera.Camera(camera_list[0], (640, 480))
    camera.start()

    # Display the camera feed
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Camera Feed")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the current camera image
        image = camera.get_image()

        # Blit the image onto the screen
        screen.blit(image, (0, 0))
        pygame.display.flip()

        yes = "Do you want to click the pic or video? "
        print(yes)
        speak(yes)
        yes = speech()
        if yes.lower() == "pic":
            image = camera.get_image()

            # Save the captured photo
            photo_path = "captured_photo.jpg"

            pygame.image.save(image, photo_path)
            print(f"Photo captured and saved as {photo_path}")
            photo = "photo captured"
            speak(photo)
    # Stop the camera
    camera.stop()

    # Ask if the user wants to play a video
    if yes.lower() == "video":
        # Create a window
        video_path = "your_video_file.mp4"  # Replace with the actual path to your video file
        pygame.display.set_caption("Video Player")
        screen = pygame.display.set_mode((800, 600))

        # Load and play the video
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.load(video_path)
        pygame.mixer.music.play()

        # Keep the window open until the video finishes playing
        while pygame.mixer.music.get_busy():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    # Quit Pygame
    video = "video captured"
    speak(video)
    pygame.quit()


def open_microsoft_office(choice):
    Ms = choice
    valid_ms = ["word", "excel", "powerpoint", "msaccess", "access", "ms access", "notepad", "power point"]
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
    valid_ms = ["manually", "speach"]
    file_to_search = next((valid for valid in valid_ms if valid in ms.lower()), None)

    if file_to_search == "manually":
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

    for i in range(min(20, len(news_headlines))):
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

    except wikipedia.exceptions.PageError:
        print("Page not found.")
        speak("Page not found")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        speak("Error Occurred")


def get_and_display_weather():
    api_key = "d1845658f92b31c64bd94f06f7188c9c"
    city = "Enter city name: "
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
def write_text():
    want = "Enter what you want typing type or copy the data or select the data or paste the data"
    print(want)
    speak(want)
    want = speech()
    if want == "type" or "typing":
        text = input("enter the text you want to enter")
        speak(text)
        pyautogui.typewrite(text, interval=0.1)
    elif want == "copy":
        pyautogui.hotkey('ctrl', 'c')
    elif want == "paste":
        pyautogui.hotkey('ctrl', 'v')
    elif want == "select":
        pyautogui.hotkey('ctrl', 'a')

def main():
    count = 0
    print("Welcome to the Assistant Program!")
    speak("Welcome to the assistant program")

    while True:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening Sir......")
            speak("Listening sir")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=10)

        try:
            choice = recognizer.recognize_google(audio)
            choice = choice.lower()
            print("You said:", choice)
        except sr.UnknownValueError:
            count = count + 1
            print("Could not understand audio")
            speak("Could not understand audio")
            if count == 3:
                print("Sorry Sir can you type your Command")
                speak("Sorry sir can you type your command")
                choice = input("Enter your Command Sir: ")
                count = 0
                speak(choice)
            continue
        except sr.RequestError as e:
            print(f"Error with the API request; {e}")
            speak("An error occurred")
            continue
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            speak("listening timed out. please try again")
            continue

        valid_choice = ["screen record", "screen recording", "screen", "audio recording", "audio record", "audio",
                        "send message on whatsapp",
                        "whatsapp", "send the message on whatsapp", "send the message on instagram", "instagram",
                        "send message on instagram",
                        "video record", "video recording", "video", "pic", "picture", "camera", "word", "excel", "powerpoint",
                        "power point", "msaccess", "ms access",
                        "notepad", "location", "email", "file", "search file", "searchfile", "search", "wikipedia", "google",
                        "facebook", "instagram",
                        "chatgpt", "telegram", "snapchat", "telegrambot", "youtube", "whatsapp", "gmail", "flipkart",
                        "amazon", "hotstar",
                        "amazonprime", "amazon prime", "netflix", "zee5", "map", "googlemap", "google map", "translate",
                        "stock", "joke", "news",
                        "reminder", "notification", "date", "time", "wikipedia", "wiki", "wiki pedia", "weather",
                        "copy", "paste", "select", "write", "text",
                        "type", "close", "bye", "exit", "goodbye", "good bye", "quit"]
        choice = next((valid for valid in valid_choice if valid in choice.lower()), None)

        if choice in ["close", "exit", "bye", "goodbye", "good bye", "quit"]:
            print("Exiting the Assistant Program. Goodbye!")
            speak("Exiting the Assistant program. goodbye")
            break
        elif choice == "screen":
            record_screen()
        elif choice == "audio":
            record_audio()
        elif choice == "whatsapp":
            send_whatsapp_message()
        elif choice == "instagram":
            instabot_actions()
        elif choice in ["video", "camera", "pic", "picture"]:
            open_camera()
        elif choice in ["word", "excel", "powerpoint", "power point", "msaccess", "ms access", "notepad"]:
            open_microsoft_office(choice)
        elif choice == "location":
            location = get_current_location()
            print("Current Location:", location)
        elif choice == "email":
            subject = input("Enter the Subject of the mail: ")
            speak(subject)
            body = input("Enter the Body of the mail: ")
            speak(body)
            to_email = input("Enter the Reciever email: " + "@gmail.com" )
            speak(to_email)
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "purvakjindal2102@gmail.com"
            sender_password = "lprn stpl tocb wqbq"
            send_email(subject, body, to_email, smtp_server, smtp_port, sender_email, sender_password)
        elif choice in ["file", "search file", "searchfile", "search"]:
            search_file()
        elif choice in ["google", "facebook", "instagram", "chatgpt", "telegram", "snapchat", "telegrambot", "youtube", "whatsapp", "gmail", "flipkart", "amazon", "hotstar", "amazonprime", "netflix", "zee5", "map", "googlemap", "google map"]:
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
        elif choice in ["text", "type", "write", "copy", "paste", "select"]:
            write_text()
        else:
            wolframalpha_query()

if __name__ == "__main__":
    main()
