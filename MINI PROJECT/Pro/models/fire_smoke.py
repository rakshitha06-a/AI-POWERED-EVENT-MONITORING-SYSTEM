import cv2
import numpy as np

def check_fire_smoke(frame):
    """
    Check for fire/smoke in the given frame
    Returns True if fire/smoke is detected, False otherwise
    """
    print("Smoke detect")
    try:
        # Resize frame for processing
        frame_resized = cv2.resize(frame, (1000, 600))
        blur = cv2.GaussianBlur(frame_resized, (15, 15), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # Fire-like color range in HSV (yellowish/orange)
        lower = np.array([22, 50, 50], dtype='uint8')
        upper = np.array([35, 255, 255], dtype='uint8')

        mask = cv2.inRange(hsv, lower, upper)
        number_of_total = cv2.countNonZero(mask)
        
        # Threshold for fire detection
        if number_of_total > 2000:
            return True
        return False
        
    except Exception as e:
        print(f"Error in fire/smoke detection: {e}")
        return False
