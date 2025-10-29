import re
import requests
import speech_recognition as sr
from enum import Enum

from question_answer import ask_professor, get_transcript, valid_question
from tts import text_to_speech
from tts_stream import text_to_speech_stream
# from video_sidebar_module import resume_video_close_sidebar, pause_video_open_sidebar
# from claude_inference_module import question_validity, get_answer
# from FastAPI_requests import send_question, send_answer
# from speech_to_text_module import text_to_speech


def clean_text_for_tts(text):
    text = text.replace('_', ' ').replace('-', ' ')
    text = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', text)

    cleaned_text = re.sub(r'[^a-zA-Z0-9.,!?: \'"]',
                          '', text, flags=re.IGNORECASE)

    text = re.sub(r'\s+', ' ', text).strip()
    return cleaned_text


class ContinuousSpeechListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.conversation = False
        self.trigger_word = "thank you"

        # Calibrate for ambient noise
        with self.microphone as source:
            print("🔧 Calibrating for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Calibration complete\n")

    def check_trigger_word(self, text):
        """Check if text contains any trigger word"""

        text_lower = text.lower()
        if self.trigger_word in text_lower:
            return True
        return False

    def process_speech(self, text):
        """Main processing logic based on conversation state"""
        print(f"\n{'='*60}")
        print(f"State: {'IN_CONVERSATION' if self.conversation else 'IDLE'}")
        print(f"Heard: '{text}'")
        print(f"{'='*60}")

        # Check for trigger word first
        if self.check_trigger_word(text):
            # resume video
            response = requests.get("http://localhost:8000/toggleVideo")
            # collapse app
            response = requests.post("http://localhost:8000/setCollapsedTrue")
            self.conversation = False
            # print("🔴 Conversation ended\n")
            return

        # Execute based on state
        if valid_question(text):
            requests.post("http://localhost:8000/chat/user/",
                          json={"text": text})
            if not self.conversation:
                # conversation = False: do thing 1 and thing 2
                # pause video
                requests.get("http://localhost:8000/toggleVideo")
                # expand app
                self.conversation = True
                requests.post(
                    "http://localhost:8000/setCollapsedFalse")
            transcript = get_transcript(mock=True)
            answer = ask_professor(transcript, text)
            requests.post("http://localhost:8000/chat/bot/",
                          json={"text": answer})
            # tts
            text_to_speech_stream(clean_text_for_tts(answer))

        print()

    def listen_continuously(self):
        with self.microphone as source:
            while True:
                try:
                    print("Listening...", end='\r')
                    # Listen for speech (blocks until speech detected)
                    audio = self.recognizer.listen(
                        source,
                        timeout=None,  # Wait indefinitely
                        phrase_time_limit=None  # Max 10 seconds per phrase
                    )

                    try:
                        # Recognize speech
                        text = self.recognizer.recognize_google(audio)
                        self.process_speech(text)

                    except sr.UnknownValueError:
                        print("❌ Couldn't understand that")
                    except sr.RequestError as e:
                        print(f"❌ Recognition error: {e}")

                except KeyboardInterrupt:
                    print("\n\n👋 Stopping listener...")
                    break
                except Exception as e:
                    print(f"Error: {e}")


# Usage
if __name__ == "__main__":
    listener = ContinuousSpeechListener()
    listener.listen_continuously()
