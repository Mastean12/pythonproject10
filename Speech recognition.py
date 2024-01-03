import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from googleapiclient.discovery import build
import pyttsx3

# YouTube API Key (replace with your own key)
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        speak("Welcome, I am ready to listen to you. Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        speak("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        speak(f"Error with the request; {e}")
        return ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def search_youtube(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query,
        part="id",
        maxResults=1
    )
    response = request.execute()
    if "items" in response and response["items"]:
        video_id = response["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        speak("No search results found on YouTube.")
        return None

def open_chrome():
    driver = webdriver.Chrome()
    return driver

def search_google(driver, query):
    driver.get("https://www.google.com/")
    search_box = driver.find_element("name", "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

def play_youtube_video(video_url):
    speak(f"Opening YouTube video: {video_url}")
    # Open the video in the default web browser
    import webbrowser
    webbrowser.open(video_url)

def main():
    while True:
        query = recognize_speech()

        if query:
            speak(f"You said: {query}")

            # Check if the query is related to YouTube
            if "youtube" in query.lower():
                video_url = search_youtube(query)
                if video_url:
                    play_youtube_video(video_url)

            # Check if the query is related to Google search
            elif "search" in query.lower() or "google" in query.lower():
                driver = open_chrome()
                search_google(driver, query)

            else:
                speak("Command not recognized.")

            satisfaction = input("Are you satisfied? (Yes/No): ").lower()

            if satisfaction == "yes":
                speak("Thank you!")
                break
            elif satisfaction == "no":
                speak("Sorry for the inconvenience caused. How can I help you?")
            else:
                speak("Invalid response. Please answer with 'Yes' or 'No'.")

if __name__ == "__main__":
    main()
