import cv2
from ultralytics import YOLO
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

def check_unconscious(frame):
    """
    Check for unconscious/fallen person in the given frame
    Returns True if unconscious person is detected, False otherwise
    """
    try:
        if not load_model():
            return False
            
        # Resize frame for processing
        frame_resized = cv2.resize(frame, (1020, 600))
        
        results = model(frame_resized)
        
        # Extract detection results
        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes.data
            if boxes is not None and len(boxes) > 0:
                for box in boxes:
                    x1, y1, x2, y2, conf, cls_id = box[:6]
                    cls_id = int(cls_id)
                    
                    # Check if detected object is a person (class 0 in COCO)
                    if cls_id == 0 and conf > 0.5:  # person with confidence > 50%
                        h = y2 - y1
                        w = x2 - x1
                        
                        # If person is horizontal (width > height), they might have fallen
                        if w > h * 1.2:  # width is 20% more than height
                            return True
                            
        return False
        
    except Exception as e:
        print(f"Error in unconscious detection: {e}")
        return False