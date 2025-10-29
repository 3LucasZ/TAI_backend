import os
import time
import subprocess  # Added for running ffplay
from dotenv import load_dotenv
from fish_audio_sdk import WebSocketSession, TTSRequest

# --- Configuration ---
# IMPORTANT: Set your API key as an environment variable for security
# On Mac/Linux: export FISH_AUDIO_API_KEY="your_key_here"
# On Windows:   set FISH_AUDIO_API_KEY="your_key_here"
#
# Or, for testing, you can uncomment the line below and paste your key:
# os.environ["FISH_AUDIO_API_KEY"] = "your_key_here"
load_dotenv()
API_KEY = os.environ.get("FISH")
# TODO: Change this to your voice model ID
VOICE_MODEL_ID = "3b04c93064834a049307060bedf42a1f"
# OUTPUT_FILENAME = "streaming_output.mp3" # No longer saving to a file

# --- IMPORTANT: FFmpeg/ffplay Requirement ---
# This script now uses 'ffplay' to play the audio stream in real-time.
# 'ffplay' is part of the FFmpeg suite.
#
# You MUST install FFmpeg and ensure 'ffplay' is in your system's PATH.
# Download: https://ffmpeg.org/download.html
#
# To check if it's installed, run this in your terminal:
# ffplay -version
# If it's not found, you'll need to install it and add it to your PATH.


def stream_text_generator(text_to_stream: str):
    """
    This is a generator function that yields the text word-by-word.
    The Fish Audio SDK will call this function to get text chunks.
    """
    print("--- Starting to stream text ---")
    words = text_to_stream.split()
    for i, word in enumerate(words):
        # Yield the word with a space to ensure natural pauses
        chunk = word + " "
        print(f"Sending chunk {i+1}/{len(words)}: '{chunk}'")
        yield chunk

        # You can add a small delay to simulate real-time typing
        # time.sleep(0.3)

    print("--- Finished streaming text ---")


def text_to_speech_stream(text):
    """
    Main function to set up and run the TTS streaming.
    """
    if not API_KEY:
        print("Error: FISH_AUDIO_API_KEY environment variable not set.")
        print("Please set the variable or paste your key directly into the script.")
        return

    if VOICE_MODEL_ID == "your_voice_model_id":
        print("Error: Please update VOICE_MODEL_ID with your actual voice model ID.")
        return

    print(f"Initializing WebSocket session...")
    # Initialize the WebSocket session with your API key
    try:
        session = WebSocketSession(API_KEY)
    except Exception as e:
        print(f"Error initializing session: {e}")
        print(
            "Please ensure your API key is correct and you have 'fish-audio-sdk' installed.")
        return

    # Create the TTSRequest object
    # The 'text' parameter is empty because we are providing text via the generator
    request = TTSRequest(
        text="hello world",
        reference_id=VOICE_MODEL_ID,
        temperature=0.7,  # Controls voice variation
        top_p=0.7,        # Controls diversity
        latency="balanced"  # Use 'balanced' for a good mix of speed and quality
    )

    # --- Set up ffplay subprocess ---
    print("Starting audio player (ffplay)...")
    # -autoexit: Quits when playback finishes
    # -nodisp: Disables the graphical display window (audio only)
    # -i - : Reads input from stdin
    ffplay_cmd = ["ffplay", "-autoexit", "-nodisp", "-i", "-"]

    try:
        player_proc = subprocess.Popen(
            ffplay_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,  # Suppress normal ffplay output
            stderr=subprocess.DEVNULL  # Suppress ffplay errors/logs
        )
    except FileNotFoundError:
        print("\n--- ERROR: 'ffplay' not found ---")
        print(
            "This script requires 'ffplay' (from FFmpeg) to be installed and in your PATH.")
        print("Please download FFmpeg from: https://ffmpeg.org/download.html")
        return
    except Exception as e:
        print(f"\nError starting ffplay: {e}")
        return

    print(f"Streaming TTS and playing in real-time...")

    # Get the generator function
    text_stream_gen = stream_text_generator(text)

    try:
        # We no longer write to a file, we write to the player's stdin
        #
        # session.tts() takes the request and the text generator
        # It returns an audio chunk generator
        for i, audio_chunk in enumerate(session.tts(request, text_stream_gen)):
            print(f"Received audio chunk {i+1}, playing...")
            try:
                # Write the audio chunk directly to ffplay's input
                player_proc.stdin.write(audio_chunk)
            except (BrokenPipeError, IOError):
                # This can happen if ffplay closes unexpectedly
                print("Player process pipe broke. Stopping stream.")
                break

        print("\n--- Stream finished! ---")

    except Exception as e:
        print(f"\nAn error occurred during streaming: {e}")
        print("Please check your API key, voice model ID, and internet connection.")

    finally:
        # --- Clean up ---
        if 'player_proc' in locals() and player_proc.stdin:
            print("Closing player stream...")
            player_proc.stdin.close()  # Signal end of stream to ffplay
            print("Waiting for player to exit...")
            player_proc.wait()  # Wait for ffplay process to terminate
            print("Playback complete.")


if __name__ == "__main__":
    text = '''
To construct a dataframe, there are several methods. As I covered starting around 00:20, one common way is using `pd.read_csv()` to read from a CSV file. You can also create one from a list with column names (around 02:34), or from a list of lists where each sub-list represents a row, along with specifying column names (around 03:07).
'''
    text_to_speech_stream(text)
