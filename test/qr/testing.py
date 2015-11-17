import numpy as np
import cv2

def read_test():
    img=cv2.imread("./fencing.png",1)

    cv2.imshow("window",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def video_test():
    cap=cv2.VideoCapture(0)

    while(True):
        ret,frame=cap.read()

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        cv2.imshow("frame",gray)
        if cv2.waitKey(1)==ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def video_test2():
    cap=cv2.VideoCapture(0)

    fourcc=cv2.cv.CV_FOURCC(*"XVID")
    out=cv2.VideoWriter("out.avi",fourcc,20.0,(640,480))

    while cap.isOpened():
        ret,frame=cap.read()
        if ret==True:
            frame=cv2.flip(frame,0)

            out.write(frame)

            cv2.imshow("frame",frame)
            if cv2.waitKey(1)==ord("q"):
                break
        else:
            break
video_test2()
