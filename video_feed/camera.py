'''

Working : Captures the frame and finds the person
    1. Main Thread recieves the frame using RTSP protocol
    2. Sub Thread runs the YOLO model 

'''



import cv2
import numpy as np
from ultralytics import YOLO
import threading

#Constants
MODEL_VERSION = "yolov8n.pt"
CAMERA_RTSP_LINK = "rtsp://192.168.43.1:8554/fpv_stream"

class Model:

    def __init__(self):
        # model initialization and variable decalration
        self.model = YOLO(MODEL_VERSION)
        self.result_img = None   # Stores Bounding Boxed Image -> Annotated frame 
        self.stop_model = False  # Flag to kill the thread
        self.live = np.zeros((300,300,3)) # Stores the Live/Current Frame

        #Threading for YOLO model
        self.prediction = threading.Thread(target=self._run_model) # Thread Initalization
        self.prediction.start() # Starts the Thread

    def _run_model(self):
        '''
        Its is a thread which runs the Model for person Detection
        '''
        # YOLO model inference
        while True :
            current_frame = self.live # Captures the live frame

            if current_frame.any(): # Valid Image
                result = self.model.predict(current_frame,verbose=False,classes = 0) # Prediction for person class 

                # result[0] has the bounding boxes
                print(f"No of Persons -> {len(result[0])}") # No of Person

            if self.stop_model: # Check for Flag
                break


def main():
    
    # Model Initialization
    model = Model() # Starts the Thread
    cam = cv2.VideoCapture(CAMERA_RTSP_LINK) # Source Setup

    while cam.isOpened():
        ret , frame = cam.read() # Get the Current Frame 
        if ret :

            frame = cv2.resize(frame,(640,480)) # Image is Resized
            model.live = frame # Updation for Thread

            # Display the Live Feed
            cv2.imshow("out",frame)
            if cv2.waitKey(1) & 0XFF == ord('q'):
                model.stop_model = True
                break
        else:
            break


    # Release the camera and destroy the windows opened
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

    


        




