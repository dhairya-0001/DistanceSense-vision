import torch
import cv2
import numpy as np
import os
from .model import SignClassifier
from torchvision import transforms
from PIL import Image

class SignRecognizer:
    def __init__(self, config):
        self.num_classes = config['sign_recognition']['num_classes']
        self.img_size = config['sign_recognition']['image_size']
        self.model_path = config['sign_recognition']['model_path']
        self.conf_threshold = config['sign_recognition']['confidence_threshold']
        
        # Determine Device
        self.device = torch.device('cpu') 
        
        self.model = SignClassifier(num_classes=self.num_classes)
        self.model.to(self.device)
        self.model.eval() # CRITICAL for inference optimization
        
        # Try to load weights if they exist
        if os.path.exists(self.model_path):
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
            print(f"Loaded trained model from {self.model_path}")
        else:
            print(f"Warning: No weights found at {self.model_path}. Using untrained classifier logic.")
            
        self.transform = transforms.Compose([
            transforms.Resize((self.img_size, self.img_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        # Mock classes for 15 classes from GTSRB
        self.classes = [
            "Speed Limit (20)", "Speed Limit (30)", "Speed Limit (50)", "Speed Limit (60)", 
            "Speed Limit (70)", "Speed Limit (80)", "Speed Limit (100)", "Speed Limit (120)",
            "Yield", "Stop", "No Entry", "Caution", "Keep Right", "Turn Left", "Turn Right"
        ]

    def recognize_sign(self, cv_image):
        # Convert cv2 BGR image to RGB PIL image
        color_coverted = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(color_coverted)
        
        input_tensor = self.transform(pil_image).unsqueeze(0).to(self.device)
        
        with torch.no_grad(): # CRITICAL for optimization
            output = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            
            # Get max probability and corresponding class index
            max_prob, class_idx = torch.max(probabilities, dim=0)
            confidence = max_prob.item()
            
            if confidence > self.conf_threshold:
                return self.classes[class_idx], confidence
            else:
                return "Unknown", confidence

    def process_frame(self, frame):
        # For a full implementation, you would first run a sign *detector* 
        # Here we mock the box for demonstration since we just do classification
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        box_size = 150
        
        x1, y1 = center_x - box_size//2, center_y - box_size//2
        x2, y2 = center_x + box_size//2, center_y + box_size//2
        
        # Crop region of interest
        roi = frame[y1:y2, x1:x2]
        
        if roi.size > 0 and roi.shape[0] > 0 and roi.shape[1] > 0:
            label, confidence = self.recognize_sign(roi)
            
            color = (0, 255, 255) # Yellow highlight bounds
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            text = f"{label} ({confidence*100:.1f}%)"
            t_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            
            # Draw semi-transparent background for text (optional but good UI)
            cv2.rectangle(frame, (x1, y1 - t_size[1] - 10), (x1 + t_size[0] + 5, y1), color, -1)
            cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
        return frame
