import cv2
import detect
import numpy as np
import zbar

def convert_to_zbar_image(image):
    """Create a zbar compatible Image object
    from a numpy array of pixels

    :image: ndarray
    :returns: zbar.Image

    """
    height=image.shape[0]
    width=image.shape[1]
    zimage=zbar.Image(width, height, "Y800", np.ndarray.tobytes(ex))

    return zimage

def qr_string_from_zimage(zimage):
    """Extract the encoded string found inside
    a given zbar Image

    :zimage: zbar.Image
    :returns: str or None

    """
    scanner=zbar.ImageScanner()
    result=scanner.scan(zimage)

    if result==0:
        return None
    else:
        for symbol in zimage:
            pass
        return symbol.data.decode(u"utf-8")

def qr_string_from_numpy(npimage):
    """Given the pixels in the form of a numpy array,
    do all the annoying conversions to zbar and
    get the string from it.

    :npimage: ndarray
    :returns: str or None

    """
    return qr_string_from_zimage(convert_to_zbar_image(npimage))

#--------------------------------------------------------------------------------#

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



    k=cv2.waitKey(10)

    if k==ord("t"):
        result=qr_string_from_numpy(ex)
        if ex is None:
            print "Could not read"
        else:
            print result

    if k==ord("q"):
        break

    #if k==ord("p"):
    #    detect._outer_triangle(detect._big_corners(corners))

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
