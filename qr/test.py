import cv2
import detect
import numpy as np
from detect import nothing
import Image
import qrtools

cap=cv2.VideoCapture(0)

k=0
imcount=0
while(k!=27):
    ret,frame=cap.read()

    l=100
    high,ex=detect.extract_and_highlight(frame,l)
    
    #ex=cv2.pyrDown(ex)
    #ex=cv2.pyrUp(ex)

    high[-l-1:-1,-l-1:-1,:]=ex[:,:,None]
    cv2.imshow("high",high)


    expil=Image.fromarray(ex)
    code=qrtools.QR(expil)
    if code.decode():
        print code.data
        print code.data_type
        print code.data_to_string()

    k=cv2.waitKey(10)

    if k==ord("p"):
        detect._outer_triangle(detect._big_corners(corners))


    if k==ord("c"):
        filename="code.jpg"
        print "Writing "+filename
        cv2.imwrite(filename,ex)

    if k==ord("s"):
        filename="squares"+str(imcount)+".jpg"
        print "Writing "+filename
        cv2.imwrite(filename,high)
        imcount+=1

cap.release()
cv2.destroyAllWindows()
