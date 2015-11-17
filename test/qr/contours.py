import cv2
import numpy as np

def nothing(x):
    pass

def create_threshslider(name):
    cv2.createTrackbar("threshold",name,0,255,nothing)
    cv2.createTrackbar("maxval",name,0,255,nothing)
    return

def threshslider_range(name):
    t=cv2.getTrackbarPos("threshold",name)
    m=cv2.getTrackbarPos("maxval",name)

    return t,m

#cv2.namedWindow("thresholds")
create_threshslider("thresholds")

cap=cv2.VideoCapture(0)

k=0
imcount=0
while(k!=27):
    ret,frame=cap.read()
    frameorig=np.copy(frame)

    #downscale and upscale to reduce noise
    frame=cv2.pyrDown(frame)
    frame=cv2.pyrUp(frame)

    gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    #blur=cv2.bilateralFilter(gray,9,75,75)
    t,m=threshslider_range("thresholds")
    
        
    ret,th2=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    th3=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,2)
    th4=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)

    edges=cv2.Canny(th2,0.5*ret,ret)

    contours,hierarchy=cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    approx=[cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True),True) for cnt in contours]


    squares=[]
    try:
        for cnt,hier in zip(contours,hierarchy[0]):
            approx=cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True),True)

            if len(approx)!=4:
                continue
            elif cv2.contourArea(approx)<100:
                continue
            elif not cv2.isContourConvex(approx):
                continue

            length=cv2.arcLength(approx,True)
            area=cv2.contourArea(approx)
            area2=(length/4)*(length/4)

            if area/area2<0.99:
                continue

            squares.append(approx)
    except:
        print "Um... yeah"
    
    cv2.drawContours(frame,squares,-1,(0,255,0),1)



    cv2.imshow("frame",frame)
    #cv2.imshow("frameorig",frameorig)
    #cv2.imshow("th1",th1)
    cv2.imshow("th2",th2)
    #cv2.imshow("th3",th3)
    #cv2.imshow("th4",th4)
    cv2.imshow("canny",edges)
    
    k=cv2.waitKey(10)

    if k==ord("p"):
        print len(squares)

    if k==ord("s"):
        filename="squares"+str(imcount)+".jpg"
        print "Writing "+filename
        cv2.imwrite(filename,frame)
        imcount+=1

cap.release()
cv2.destroyAllWindows()
