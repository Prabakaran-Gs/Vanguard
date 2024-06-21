import cv2
import numpy as np
from ultralytics import YOLO
import threading

#Constants
MODEL_VERSION = "yolov8n.pt"
CAMERA_RTSP_LINK = "rtsp://192.168.43.1:8554/fpv_stream"

class Model:

    def __init__(self):
        self.model = YOLO(MODEL_VERSION)
        self.result_img = None
        self.stop_model = False
        self.live = np.zeros((300,300,3))

        self.prediction = threading.Thread(target=self.run_model)
        self.prediction.start()

    def run_model(self):
        while True :
            current_frame = self.live

            if current_frame.any():
                result = self.model.predict(current_frame,verbose=False,classes = 0)
                print(f"No of Persons -> {len(result[0])}")

            if self.stop_model:
                break


def main():
    model = Model()
    cam = cv2.VideoCapture(CAMERA_RTSP_LINK)

    while True:
        ret , frame = cam.read()
        frame = cv2.resize(frame,(640,480))
        if ret :
            model.live = frame
            cv2.imshow("out",frame)
            if cv2.waitKey(1) & 0XFF == ord('q'):
                model.stop_model = True
                break
        else:
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

    


        




