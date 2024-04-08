import cv2 as cv 

cam = cv.VideoCapture("rtsp://172.16.30.159:8080/h264_ulaw.sdp")

while True:
    ret , frame = cam.read()
    if ret :
        cv.imshow("out",frame)

        if cv.waitKey(1) & 0XFF == ord('q'):
            break
    else:
        break

cam.release()
cv.destroyAllWindows()