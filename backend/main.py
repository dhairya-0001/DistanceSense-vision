import os
import sys

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cv2
import time
import os
import yaml

from distance_module.distance_estimator import DistanceEstimator
from sign_module.inference import SignRecognizer

# Ensure required directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("frontend/templates", exist_ok=True)
os.makedirs("frontend/static", exist_ok=True)

app = FastAPI(title="DriveSense AI")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Load Configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Initialize Modules
distance_estimator = DistanceEstimator(config)
sign_recognizer = SignRecognizer(config)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy", "modules": ["distance_estimation", "sign_recognition"]}

# --- Video Streaming Generators ---

def generate_distance_frames():
    cap = cv2.VideoCapture(0) # Use 0 for webcam
    if not cap.isOpened():
        raise RuntimeError("Could not initiate webcam")

    frame_skip = config['system'].get('frame_skip', 2)
    frame_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        # Process frame
        start_time = time.time()
        processed_frame = distance_estimator.process_frame(frame)
        fps = 1.0 / (time.time() - start_time)
        
        cv2.putText(processed_frame, f"FPS: {fps:.1f}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

def generate_sign_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not initiate webcam")

    frame_skip = config['system'].get('frame_skip', 2)
    frame_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        # Process frame
        start_time = time.time()
        processed_frame = sign_recognizer.process_frame(frame)
        fps = 1.0 / (time.time() - start_time)
        
        cv2.putText(processed_frame, f"FPS: {fps:.1f}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)

        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.get("/distance-video")
async def distance_video():
    return StreamingResponse(generate_distance_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/video_feed")
async def video_feed():
    # Alias /video_feed to distance video as commonly requested
    return StreamingResponse(generate_distance_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/sign-video")
async def sign_video():
    return StreamingResponse(generate_sign_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.post("/sign-image")
async def analyze_sign_image(file: UploadFile = File(...)):
    # Load image bytes, route to recognizer, return JSON
    return {"message": "Image analysis endpoint ready for implementation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
