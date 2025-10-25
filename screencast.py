import time
import mss
import numpy as np
import cv2
import pyautogui
import findvideo  # Assuming you have this module
import uvicorn
import threading
from fastapi import FastAPI

# --- Configuration ---
FPS = 10
FRAME_DURATION = 1.0 / FPS

# --- Shared State & Threading Lock ---
shared_state = {
    "cx": None,
    "cy": None
}
state_lock = threading.Lock()

# --- FastAPI ---
app = FastAPI()


@app.get("/toggleVideo")
def toggleVideo():
    # Use lock to safely read from the shared state
    with state_lock:
        response = {
            "cx": shared_state["cx"],
            "cy": shared_state["cy"]
        }
    pyautogui.moveTo(response["cx"], response["cy"])
    pyautogui.leftClick()

    # pyautogui.press('x')
    # pyautogui.press('f8')
    # pyautogui.keyDown('fn')
    pyautogui.press('f8')
    # pyautogui.keyUp('fn')

    # pyautogui.leftClick()
    # pyautogui.click(response["cx"], response["cy"])
    return response

# --- Screen Capture Loop ---


def run_screen_capture():
    global shared_state

    sct = mss.mss()
    monitor = sct.monitors[1]
    cur = time.time()

    try:
        while True:
            if time.time() - cur > FRAME_DURATION:
                screenshot = sct.grab(monitor)
                img = np.array(screenshot)
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                _, cx, cy = findvideo.find_video(frame)

                with state_lock:
                    shared_state["cx"] = cx
                    shared_state["cy"] = cy

                cur = time.time()
    except Exception as e:
        print(f"Error in screen capture loop: {e}")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Create the background thread for screen capture
    # daemon=True means this thread will automatically exit
    # when the main program (FastAPI) exits.
    capture_thread = threading.Thread(
        target=run_screen_capture,
        daemon=True
    )
    # Start the background thread
    print("Starting screen capture thread...")
    capture_thread.start()

    # Run the FastAPI server in the main thread
    #    This will block until you press Ctrl+C in the terminal
    print(f"Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
