import os
import torch
from ultralytics import YOLO

def load_detection_model():
    """Builds/Loads the object detection model."""
    os.makedirs("models", exist_ok=True)
    # Using YoloV8n (nano) which is highly optimized for CPU
    model = YOLO("models/yolov8n.pt") 
    return model
