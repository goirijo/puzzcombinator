import cv2
import detect
import numpy as np
from detect import nothing

cap=cv2.VideoCapture(0)

k=0
imcount=0
while(k!=27):
    ret,frame=cap.read()

    l=100
    high,ex=detect.extract_and_highlight(frame,l)
    high[-l-1:-1,-l-1:-1,:]=ex[...]

    cv2.imshow("high",high)

    k=cv2.waitKey(10)

    if k==ord("p"):
        detect._outer_triangle(detect._big_corners(corners))


    if k==ord("s"):
        filename="squares"+str(imcount)+".jpg"
        print "Writing "+filename
        cv2.imwrite(filename,frame)
        imcount+=1

cap.release()
cv2.destroyAllWindows()
