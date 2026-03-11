import cv2

def resize_frame(frame, width=640, height=480):
    """Utility to resize frames for optimization."""
    return cv2.resize(frame, (width, height))

def add_hud(frame, text, position):
    """Draws HUD style text on frame."""
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    return frame
