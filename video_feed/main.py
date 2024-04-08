import cv2
import time
from ultralytics import YOLO
import threading

model = YOLO("yolov8n.pt")

def predict(frame):
    result = model.predict(frame,verbose=False,classes = 0)
    print(f"No of Persons -> {len(result[0])}")

# Function to capture frames from video and save them
def capture_frames(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    k = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        count += 1
        if count % (frame_rate * 2) == 0:  # Capture frame every 2 seconds
            cv2.imwrite(f"frame_{k}.jpg", frame)
            k+=1
            count = 0
            # Thread prediction function
            prediction_thread = threading.Thread(target=predict, args=(frame,))
            prediction_thread.start()

    cap.release()

# Example usage
video_path = "rtsp://172.16.30.159:8080/h264_ulaw.sdp"
output_path = 'output'
capture_frames(video_path, output_path)