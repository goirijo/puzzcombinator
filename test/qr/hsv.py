import cv2
import numpy as np

def nothing(x):
    pass

def create_rgbslider(name):
    cv2.createTrackbar("r",name,0,255,nothing)
    cv2.createTrackbar("g",name,0,255,nothing)
    cv2.createTrackbar("b",name,0,255,nothing)
    return

def rgbslider_range(name):
    r=cv2.getTrackbarPos("r",name)
    g=cv2.getTrackbarPos("g",name)
    b=cv2.getTrackbarPos("b",name)

    return r,g,b


cap=cv2.VideoCapture(0)

maximg=np.zeros((300,512,3),np.uint8)
minimg=np.zeros((300,512,3),np.uint8)
cv2.namedWindow("max")
cv2.namedWindow("min")

create_rgbslider("max")
create_rgbslider("min")

k=0
while(k!=27):
    ret,frame=cap.read()

    cv2.imshow("max",maximg)
    cv2.imshow("min",minimg)
    r1,g1,b1=rgbslider_range("max")
    r0,g0,b0=rgbslider_range("min")
    maximg[:]=[b1,g1,r1]
    minimg[:]=[b0,g0,r0]

    maxvals=np.array([r1,g1,b1])
    minvals=np.array([r0,g0,b0])


    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,minvals,maxvals)
    res=cv2.bitwise_and(frame,frame,mask=mask)

    cv2.imshow("hsv",hsv)
    cv2.imshow("frame",frame)
    cv2.imshow("res",res)
    
    k=cv2.waitKey(10)

cap.release()
cv2.destroyAllWindows()
