import os
from .model_loader import load_detection_model

class DistanceEstimator:
    def __init__(self, config):
        self.focal_length = config['camera']['focal_length']
        self.real_vehicle_width_m = config['camera']['real_vehicle_width_m']
        self.conf_threshold = config['camera']['confidence_threshold']
        
        # Load YOLOv8 Nano model
        self.model = load_detection_model()

    def process_frame(self, frame):
        import cv2
        # Use simple cv2 operations here as model returns results
        results = self.model(frame, verbose=False, device='cpu', conf=self.conf_threshold)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Class 2 is 'car', 5 is 'bus', 7 is 'truck' in COCO dataset
                cls_id = int(box.cls[0])
                if cls_id in [2, 5, 7]:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    pixel_width = x2 - x1
                    
                    if pixel_width > 0:
                        # Monocular distance estimation
                        distance = (self.real_vehicle_width_m * self.focal_length) / pixel_width
                        
                        # Draw bounding box and distance label
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        label = f"Dist: {distance:.2f}m"
                        
                        # Text background
                        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                        cv2.rectangle(frame, (x1, y1 - t_size[1] - 10), (x1 + t_size[0] + 5, y1), (255, 0, 0), -1)
                        cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        
        return frame
