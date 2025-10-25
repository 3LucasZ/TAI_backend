import speech_recognition as sr
import time
from enum import Enum


class ConversationState(Enum):
    IDLE = "idle"
    IN_CONVERSATION = "in_conversation"


class ContinuousSpeechListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.conversation = False
        self.trigger_word = "thank you"
        self.question_starters = ["who", "what", "where", "when", "why", "how", "is", "are",
                                  "do", "does", "can", "could", "will", "would", "should", "shall", "may", "might"]

        # Calibrate for ambient noise
        with self.microphone as source:
            print("🔧 Calibrating for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("✅ Calibration complete\n")

    def thing_1(self, text):
        """Execute when conversation=False and speech detected"""
        print(f"[THING 1] Processing: {text}")
        self.conversation = True
        # Your logic here
        if any(text.lower().startswith(word) for word in self.question_starters):
            return True

    def thing_2(self, text):
        """Execute on every speech detection"""
        print(f"[THING 2] Processing: {text}")
        # Your logic here
        pass

    def thing_3(self, text):
        """Execute on trigger word"""
        print(f"[THING 3] Trigger detected: {text}")
        # Your logic here
        pass

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
            self.thing_3(text)
            self.conversation = False
            print("🔴 Conversation ended\n")
            return

        # Execute based on state
        if not self.conversation:
            # conversation = False: do thing 1 and thing 2
            self.thing_1(text)
            self.thing_2(text)
        else:
            # conversation = True: do only thing 2
            self.thing_2(text)

        print()

    def listen_continuously(self):
        """Continuously listen for speech"""
        print("🎤 Continuous listener started")
        print(f"   Trigger words: {', '.join(self.trigger_word)}")
        print("   Press Ctrl+C to stop\n")

        with self.microphone as source:
            while True:
                try:
                    print("👂 Listening...", end='\r')

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
listener = ContinuousSpeechListener()
listener.listen_continuously()
