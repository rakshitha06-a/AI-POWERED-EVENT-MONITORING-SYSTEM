from ultralytics import YOLO
import cv2
import numpy as np

# Load YOLOv8 model (load once, reuse)
model = None

def load_model():
    """Load the YOLO model once"""
    global model
    if model is None:
        try:
            model = YOLO("yolov8n.pt")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            return False
    return True

def check_crowd_surge(frame):
    """
    Check for crowd surge in the given frame
    Returns True if crowd surge is detected, False otherwise
    """
    try:
        if not load_model():
            return False
            
        # Threshold for people per segment
        OVER_CROWD_THRESHOLD = 2
        
        # Grid size (rows x cols)
        ROWS, COLS = 3, 3
        
        height, width, _ = frame.shape
        segment_counts = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        # Run YOLOv8
        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if cls == 0:  # person
                    xyxy = box.xyxy[0].cpu().numpy().astype(int)
                    cx = int((xyxy[0] + xyxy[2]) / 2)
                    cy = int((xyxy[1] + xyxy[3]) / 2)

                    row = min(ROWS - 1, cy * ROWS // height)
                    col = min(COLS - 1, cx * COLS // width)
                    segment_counts[row][col] += 1

        # Check if any segment has too many people
        for i in range(ROWS):
            for j in range(COLS):
                if segment_counts[i][j] >= OVER_CROWD_THRESHOLD:
                    return True
                    
        return False
        
    except Exception as e:
        print(f"Error in crowd surge detection: {e}")
        return False