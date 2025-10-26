import requests
import pygame
import io
import time
from fish_audio_sdk import WebSocketSession, TTSRequest
import re
FISH_API_KEY = "4691bc0e3869458b9cb7e8fa91cc2941"

session = WebSocketSession(FISH_API_KEY)

voices = {"arnav": "6e445b37225c4b8baa00a50296d93ffa",
          "arnold": "536d3a5e000945adb7038665781a4aca",
          "josh": "3b04c93064834a049307060bedf42a1f"}

headers = {
    "Authorization": f"Bearer {FISH_API_KEY}",
    "Content-Type": "application/json",
    "model": "s1"
}


def clean_text_for_tts(text):
    cleaned_text = re.sub(r'[^a-zA-Z0-9.,!?: \'"]',
                          '', text, flags=re.IGNORECASE)
    return cleaned_text


def text_to_speech(text):
    url = "https://api.fish.audio/v1/tts"
    data = {
        "text": clean_text_for_tts(text),
        "format": "mp3",
        "reference_id": voices["josh"],
        "latency": "balanced"  # faster
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise error for bad status codes

        pygame.mixer.init()
        audio_buffer = io.BytesIO(response.content)
        pygame.mixer.music.load(audio_buffer)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    text = '''
To construct a dataframe, there are several methods. As I covered starting around 00:20, one common way is using `pd.read_csv()` to read from a CSV file. You can also create one from a list with column names (around 02:34), or from a list of lists where each sub-list represents a row, along with specifying column names (around 03:07).
'''
    text_to_speech(text)
