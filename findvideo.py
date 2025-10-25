import numpy as np
import cv2


def find_video(frame):
    lower_bound = np.array([0, 0, 0])
    upper_bound = np.array([240, 240, 240])  # Anything not "bright white"

    # Create a mask for non-white pixels
    mask = cv2.inRange(frame, lower_bound, upper_bound)
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    # The largest contour should be the video player
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area_threshold = 50000
    max_area_threshold = 5000000
    contours = [cnt for cnt in contours if min_area_threshold <
                cv2.contourArea(cnt) < max_area_threshold]
    if not contours:
        print("No video player found")
        return
    largest_contour = max(contours, key=cv2.contourArea)
    print("contours:", len(contours))

    # debug
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(rgb_mask, (x, y), (x+w, y+h), (0, 0, 255), 20)

    # 4. Create a function to click the middle of the video screen
    # Calculate the center of the bounding box
    # center_x = x + w // 2
    # center_y = y + h // 2
    return rgb_mask
