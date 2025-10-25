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
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    min_area_threshold = 10000
    max_area_threshold = 1000000
    best_contour = None
    best_contour_area = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w * h > max_area_threshold:
            continue
        if best_contour is None or w * h > best_contour_area:
            best_contour = c
            best_contour_area = w * h

    if best_contour is None:
        print("No video player found")
        return rgb_mask, -1, -1

    # debug
    x, y, w, h = cv2.boundingRect(best_contour)
    cv2.rectangle(rgb_mask, (x, y), (x+w, y+h), (0, 0, 255), 20)
    center_x = x + w // 2
    center_y = y + h // 2
    cv2.rectangle(rgb_mask, (center_x, center_y),
                  (center_x, center_y), (0, 0, 255), 50)
    return rgb_mask, center_x, center_y
