import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import webbrowser
import pyttsx3
import subprocess
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init('sapi5')

# Function to listen for user input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language='en-IN')
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError as e:
            return f"Sorry, there was a problem with the request: {e}"

# Spotify API credentials
CLIENT_ID = '13c6e2436fb64146bc6cd00f626418b7'
CLIENT_SECRET = '9a084886259943768eb7c1771a3dd74d'

# Function to authenticate and get access token
def get_access_token():
    scope = 'user-read-private user-top-read'
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='https://localhost:8000', scope=scope)
    auth_url = sp_oauth.get_authorize_url()
    print(f"Please visit {auth_url} and authorize the app.")
    # Open a web browser to the authorization URL
    webbrowser.open(auth_url)
    # Wait for user input (usually, it's a code from the web page)
    code = input("Enter the code: ")
    token = sp_oauth.get_access_token(code)
    return token

# Function to search for a song on Spotify and play it
def play_song_on_spotify(song_name):
    access_token = get_access_token()
    sp = spotipy.Spotify(auth=access_token)

    # Search for the song
    results = sp.search(q=song_name, type='track', limit=1)
    if len(results['tracks']['items']) > 0:
        track = results['tracks']['items'][0]
        print(f"Playing {track['name']} by {track['artists'][0]['name']}")
        sp.play(track_uri=track['uri'])
    else:
        engine.say("Sorry, I couldn't find the song.")
        engine.runAndWait()

# Main function to process user commands
def main():
    while True:
        # Wake up only when "hello" is said
        command = listen().strip()
        if 'hello' in command:
            engine.say("Hello! How can I assist you?")
            engine.runAndWait()

            # Process the rest of the commands as usual
            while True:
                command = listen().strip()
                if 'goodbye' in command:
                    engine.say("Goodbye!")
                    engine.runAndWait()
                    break
                elif 'search and play song on spotify' in command:
                    song_name = command.replace('search and play song on spotify', '').strip()
                    if song_name:
                        play_song_on_spotify(song_name)
                    else:
                        engine.say("Please specify a song name.")
                elif 'open' in command:
                    app_name = command.replace('open', '').strip()
                    open_app(app_name)

if __name__ == "__main__":
    main()
