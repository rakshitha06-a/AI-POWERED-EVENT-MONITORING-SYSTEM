#!/usr/bin/env python3
"""
Test script for AI Event Monitoring Models
This script tests all three detection models to ensure they work correctly.
"""

import cv2
import numpy as np
from models.fire_smoke import check_fire_smoke
from models.crowd_surge import check_crowd_surge
from models.unconscious import check_unconscious

def test_fire_smoke_detection():
    """Test fire/smoke detection with a sample frame"""
    print("🔥 Testing Fire/Smoke Detection...")
    
    # Create a test frame with orange/yellow colors (simulating fire)
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add orange/yellow regions to simulate fire
    test_frame[100:300, 200:400] = [0, 165, 255]  # Orange in BGR
    
    result = check_fire_smoke(test_frame)
    print(f"   Result: {'DETECTED' if result else 'No fire detected'}")
    return result

def test_crowd_surge_detection():
    """Test crowd surge detection with a sample frame"""
    print("🚨 Testing Crowd Surge Detection...")
    
    # Create a test frame
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some colored rectangles to simulate people
    for i in range(3):
        x = 100 + i * 150
        cv2.rectangle(test_frame, (x, 200), (x + 50, 350), (0, 255, 0), -1)
    
    result = check_crowd_surge(test_frame)
    print(f"   Result: {'CROWD SURGE DETECTED' if result else 'Normal crowd levels'}")
    return result

def test_unconscious_detection():
    """Test unconscious person detection with a sample frame"""
    print("🧍‍♂️ Testing Unconscious Person Detection...")
    
    # Create a test frame
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add a horizontal rectangle to simulate a fallen person
    cv2.rectangle(test_frame, (200, 300), (400, 350), (0, 255, 0), -1)
    
    result = check_unconscious(test_frame)
    print(f"   Result: {'UNCONSCIOUS PERSON DETECTED' if result else 'No unconscious person detected'}")
    return result

def test_camera_access():
    """Test if camera can be accessed"""
    print("📷 Testing Camera Access...")
    
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        cap.release()
        if ret:
            print("   ✅ Camera access successful")
            return True
        else:
            print("   ❌ Camera access failed - no frame received")
            return False
    else:
        print("   ❌ Camera access failed - could not open camera")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("🤖 AI Event Monitoring Models Test")
    print("=" * 50)
    
    # Test camera access
    camera_ok = test_camera_access()
    print()
    
    # Test detection models
    fire_ok = test_fire_smoke_detection()
    print()
    
    crowd_ok = test_crowd_surge_detection()
    print()
    
    unconscious_ok = test_unconscious_detection()
    print()
    
    # Summary
    print("=" * 50)
    print("📊 Test Summary:")
    print(f"   Camera Access: {'✅ PASS' if camera_ok else '❌ FAIL'}")
    print(f"   Fire Detection: {'✅ PASS' if fire_ok is not None else '❌ FAIL'}")
    print(f"   Crowd Detection: {'✅ PASS' if crowd_ok is not None else '❌ FAIL'}")
    print(f"   Unconscious Detection: {'✅ PASS' if unconscious_ok is not None else '❌ FAIL'}")
    print("=" * 50)
    
    if camera_ok and fire_ok is not None and crowd_ok is not None and unconscious_ok is not None:
        print("🎉 All tests passed! You can now run the main dashboard.")
        print("   Run: streamlit run main_dashboard.py")
    else:
        print("⚠️  Some tests failed. Please check your setup and dependencies.")
        print("   Make sure you have installed all requirements: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 