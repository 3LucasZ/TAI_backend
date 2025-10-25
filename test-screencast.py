import random
import time
import mss
import numpy as np
import cv2
import findvideo

fps = 10
sct = mss.mss()
monitor = sct.monitors[1]
frame_duration = 1.0 / fps
cur = time.time()
dbg = True
window_name = "TAI"
cv2.namedWindow(window_name)
cv2.moveWindow(window_name, 800, 800)

if __name__ == "__main__":
    while True:
        if time.time() - cur > frame_duration:
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            mask, cx, cy = findvideo.find_video(frame)
            mask = cv2.resize(mask, (0, 0), fx=0.25, fy=0.25)
            cv2.imshow(window_name, mask)
            cur = time.time()

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()
