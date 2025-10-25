import random
import time
import mss
import numpy as np
import cv2
import findvideo

fps = 1
frame_duration = 1.0 / fps
cur = time.time()
if __name__ == "__main__":
    while True:
        if time.time() - cur > frame_duration:
            img = cv2.imread("screenshot.png")
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            dbg_mask = findvideo.find_video(frame)
            cv2.imshow("TAI", dbg_mask)
            cur = time.time()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()
