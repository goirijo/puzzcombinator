import cv2
import random
import glob
import math
import numpy as np

jpgnamelist=glob.glob("./IMG_*.JPG")

#load list of images
imglist=[]

for name in jpgnamelist:
    img=cv2.imread(name)
    imglist.append(img)

#determine the maximum width and height of all images
maxrows=0
maxcols=0
maxchannel=0
for img in imglist:
    rows,cols,channels=img.shape
    if maxrows<rows:
        maxrows=rows
    if maxcols<cols:
        maxcols=cols
    if maxchannel<channels:
        maxchannel=channels

#make an empty image big enough to fit all images
coldims=math.ceil(math.sqrt(len(imglist)))
collage=np.zeros((coldims*maxrows,coldims*maxcols,maxchannel))

print collage.shape

#stamp in images one at a time
for x in range(int(coldims)):
    for y in range(int(coldims)):
        if len(imglist)==0:
            break

        xidx=x*maxrows
        yidx=y*maxcols
        imgidx=random.randrange(0,len(imglist))
        img=imglist.pop(imgidx)
        rows,cols,chans=img.shape

        x0=xidx
        x1=xidx+rows
        y0=yidx
        y1=yidx+cols

        print x0,x1,y0,y1

        collage[x0:x1,y0:y1,:]=img

collage=cv2.imwrite("test.jpg",collage)
