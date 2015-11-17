import cv2
import itertools
import numpy as np

def nothing(x):
    pass

def _squares(rawimg):
    """Convert given image to gray and split with adaptove
    thresholding to
    detect edges. Filter out contours that are square like
    and return them along with their hierarchy.

    :rawimg: cv2 image
    :returns: list of edges, list of hierarchy

    """
    #Downscale and rescale to remove noise
    frame=cv2.pyrDown(rawimg)

    #lose colors
    gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    frame=cv2.pyrUp(gray)

    #Use Otsu threshold to make binary
    #ret,otsu=cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #Use adaptive threshold to make binary
    adaptive=cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,3)
    cv2.adaptiveThreshold


    #find the edges
    edges=cv2.Canny(adaptive,0,255)

    #cv2.imshow("adaptive",adaptive)
    #cv2.imshow("gray",gray)
    #cv2.imshow("edges",edges)

    #Approximate the contours into polygons
    contours,hierarchy=cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    squares=[]
    hiersq=[]
    for cnt,hier in zip(contours,hierarchy[0]):
        approx=cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True),True)

        if len(approx)!=4:
            continue
        elif cv2.contourArea(approx)<200:
            continue
        elif not cv2.isContourConvex(approx):
            continue

        length=cv2.arcLength(approx,True)
        area=cv2.contourArea(approx)
        area2=(length/4)*(length/4)

        if area/area2<0.9:
            continue

        squares.append(approx)
        hiersq.append(hier)

    return squares,hiersq

def centroid(contour):
    """Compute the center of a polygon

    :moment: contour
    :returns: int,int

    """
    m=cv2.moments(contour)
    return (int(m["m10"]/m["m00"]),int(m["m01"]/m["m00"]))

def _argcorners(squares):
    """Run through a list of edges and determine which
    ones are part of the three QR code corners. Expects
    an educated set of edges such as given by _squares.
    The function computes the center of mass for each
    square and considers a corner found when 6 squares
    share a center of mass.

    :squares: list of square contours
    :returns: 3x6 array of indices

    """
    centroids=[centroid(s) for s in squares]
    inds=range(0,len(squares))

    centrinds=zip(centroids,inds)

    if len(centroids)==0:
        return []

    
    centrinds=sorted(centrinds)
    grouped=[[centrinds[0][0]]]
    groupind=[[centrinds[0][1]]]

    #Group squares by their center
    maxpixel=10
    for cent,ind in centrinds[1:]:
        if abs(cent[0]-grouped[-1][-1][0])<maxpixel and abs(cent[1]-grouped[-1][-1][1])<maxpixel:
            grouped[-1].append(cent)
            groupind[-1].append(ind)
        else:
            grouped.append([cent])
            groupind.append([ind])


    #Only a QR corner if it caught all six boxes of a corner
    corners=[]
    for group in groupind:
        if len(group)==6:
            corners.append(group)

    #Only found the corners if you got all three
    if len(corners)==3:
        return np.array(corners)

    else:
        return []

def _unrolled_corners(corners):
    """TODO: Docstring for _unrolled_corners.

    :corners: 3x6 list of list of contours
    :returns: list of contours

    """
    return [val for sublist in corners for val in sublist]

def _big_corners(corners):
    """Return only the largest box of each of
    the three corners

    :corners: list of list of contours
    :returns: list of contours

    """
    areas=[[cv2.contourArea(cnt) for cnt in sublist] for sublist in corners]
    winners=[a.index(max(a)) for a in areas]
    biggies=[]
    for c,w in zip(corners,winners):
        biggies.append(c[w])
    return biggies

def _argsort(biggies):
    """Return the given list of corners in a
    particular order:
    
    0    1

    2

    :corners: list of three contours (outer boxes of corners)
    :returns: list of indices

    """
    centers=np.array([centroid(big) for big in biggies])
    
    sortind=[]

    #First find the corner that forms 90 degrees when connected with the other two
    dots=[]
    for ref,ind1,ind2 in zip((0,1,2),(2,0,1),(1,2,0)):
        delta1=centers[ind1]-centers[ref]
        delta1=delta1/np.linalg.norm(delta1)

        delta2=centers[ind2]-centers[ref]
        delta2=delta2/np.linalg.norm(delta2)
        
        dot=np.dot(delta1,delta2)
        dots.append(abs(dot))
    
    rightangle=dots.index(min(dots))
    sortind.append(rightangle)

    #Get one of the other corners and determine position from dot product
    ref=rightangle
    ind1=(rightangle+1)%3
    ind2=(rightangle+2)%3

    delta1=centers[ind1]-centers[ref]
    delta1=delta1/np.linalg.norm(delta1)

    delta2=centers[ind2]-centers[ref]
    delta2=delta2/np.linalg.norm(delta2)

    xaxis=np.array([1,0])
    yaxis=np.array([0,1])

    d=np.array([delta1,delta2]).T
    v=np.array([xaxis,yaxis]).T
    M=np.dot(v,np.linalg.inv(d))


    if np.linalg.det(M)>0:
        sortind.append(ind1)
        sortind.append(ind2)

    else:
        sortind.append(ind2)
        sortind.append(ind1)

    return sortind

def _corners(squares,unroll=False):
    """TODO: Find the QR corners and return the
    actual polygons instead of the indices

    :squares: list of square contours
    :unroll: bool
    :returns: 3x6 array of squares, or 1d list if unroll==True

    """
    corninds=_argcorners(squares)
    
    corners=[]
    for ci in corninds:
        corner=[]
        for i in ci:
            corner.append(squares[i])
        corners.append(corner)

    if(len(corners)==3):
        sortind=_argsort(_big_corners(corners))
        corners=[corners[ind] for ind in sortind]

    if unroll:
        return _unrolled_corners(corners)
    else:
        return corners


def _corner_centers(corners):
    """Calculate the position of the center of
    the three corners of the QR code

    :squares: list of corner contours
    :returns: list of points ready for poly drawing

    """
    centers=[]
    for corn in corners:
        center=np.array([0,0])
        for box in corn:
            tcent=np.array(centroid(box))
            center+=tcent
        center=center/6.0
        centers.append(center)
    
    pts=np.array(centers,np.int32)
    pts=pts.reshape((-1,1,2))
    return [pts]

def _outer_triangle(biggies):
    """Determine the outermost corners of the
    three corner boxes, given the three corners
    boxes. Please feed sorted corners.

    :biggies: list of three contours
    :returns: list of three tuples (x,y)

    """
    centers=np.array([centroid(cnt) for cnt in biggies])

    vec1=centers[1]-centers[0]
    vec1=vec1/np.linalg.norm(vec1)
    vec2=centers[2]-centers[0]
    vec2=vec2/np.linalg.norm(vec2)

    corners=[]

    #Find the outer corner of the 90 degree corner (1st corner)
    for corn in biggies[0]:
        corn=corn[0]
        c=corn-centers[0]
        if(np.dot(vec1,c)<0 and np.dot(vec2,c)<0):
            corners.append(tuple(corn))

    #Find outermost corner for the second corner: largest dot product and length
    normlenghts=[]
    for corn in biggies[1]:
        corn=corn[0]
        c=corn-corners[0]
        #tuple of dot,length,corner
        normlenghts.append((np.dot(vec1,c/np.linalg.norm(c)),np.linalg.norm(c),tuple(corn)))

    #largest dot products are the last two
    normlenghts=sorted(normlenghts)

    #pick the longest one of the two
    if normlenghts[-1][1]>normlenghts[-2][1]:
        corners.append(normlenghts[-1][2])
    else:
        corners.append(normlenghts[-2][2])

    #Find the last corner
    normlenghts=[]
    for corn in biggies[2]:
        corn=corn[0]
        c=corn-corners[0]
        #tuple of dot,length,corner
        normlenghts.append((np.dot(vec2,c/np.linalg.norm(c)),np.linalg.norm(c),tuple(corn)))

    #largest dot products are the last two
    normlenghts=sorted(normlenghts)

    #pick the longest one of the two
    if normlenghts[-1][1]>normlenghts[-2][1]:
        corners.append(normlenghts[-1][2])
    else:
        corners.append(normlenghts[-2][2])


    return corners

def _intersection(p1p2,p3p4):
    """Get the intersection point of two lines
    given two points from each line

    :p1p2: [[x1,y1],[x2,y2]]
    :p3p4: [[x3,y3],[x4,y4]]
    :returns: [int,int]

    """

    da=p1p2[1]-p1p2[0]
    db=p3p4[1]-p3p4[0]
    dp=p1p2[1]-p3p4[0]

    dap=np.empty_like(da)
    dap[0]=-da[1]
    dap[1]=da[0]

    denom=np.dot(dap,db)
    num=np.dot(dap,dp)

    exact=(num / denom.astype(float))*db + p3p4[0]  
    #return tuple(exact.astype(int))
    return exact

def _corner_dots(biggies,outertri,ind):
    """Compute the dot products at a particular corner
    to help orient the biggie. The computed vector has the
    actual corner as a starting point and the three
    remaining box corners as possible end points.
    The "small" vector (biggie corners) are dotted with
    the vector made by the two remaining outer triangle
    corners.

    0   1

    2

    :biggies: list of three contours
    :outertri: list of three tuples (x,y)
    :ind: int, which biggie to look at
    :returns: list of (dot-product,biggie-corner)

    """
    refv=outertri[ind-1]-outertri[ind-2]
    dotcorn=[]
    for corn in biggies[ind]:
        corn=corn[0]
        if np.allclose(corn,outertri[ind]):
            continue
        v=corn-outertri[ind]
        dotcorn.append((abs(np.dot(v/np.linalg.norm(v),refv/np.linalg.norm(refv))),corn))

    #first entry is most perpendicular, last entry is most parallel
    dotcorn=sorted(dotcorn,key=lambda x: x[0])
    return dotcorn

def _outer_quad(biggies):
    """Infer the fourth point of the QR
    code to get four corners. Please feed
    presorted corner boxes:

    0   3

    1   2

    Note that the order differs from the outer
    triangle method! This is so that the contours
    don't cross if you draw them.

    :biggies: list of three contours
    :returns: list of four points

    """
    if len(biggies)==0:
        return np.array([])

    outertri=np.array(_outer_triangle(biggies))

    #Using outer triangle notation
    #Get bottom right corner of upper left box (0) (diagonal)
    dotcorn=_corner_dots(biggies,outertri,0)
    edge=dotcorn[0][1]
    p1p2=np.array([outertri[0],edge])

    #Get the bottom right corner of the upper right box (1) (vertical)
    dotcorn=_corner_dots(biggies,outertri,1)
    edge=dotcorn[2][1]
    p3p4=np.array([outertri[1],edge])

    #Get bottom right corner of lower left box (2) (horizontal)
    dotcorn=_corner_dots(biggies,outertri,2)
    edge=dotcorn[2][1]
    p5p6=np.array([outertri[2],edge])

    fourth0=_intersection(p1p2,p3p4)
    fourth1=_intersection(p1p2,p5p6)
    fourth2=_intersection(p3p4,p5p6)

    fourth=(fourth0+fourth1+fourth2)/3

    complete=np.vstack((outertri,fourth))
    resorted=np.asarray(complete[[0,2,3,1]],dtype=np.int32)

    return resorted


def _corner_highlight(frame,corners,opacity=0.3):
    """Highlight the detected corners of the QR
    code with different colors

    :frame: cv2 image
    :corners: list of QR corner contours
    :opacity: float
    :returns: cv2 image

    """
    dupe=frame.copy()
    biggies=_big_corners(corners)
    quad=_outer_quad(biggies)
    #blue,green,red
    bgr=[(255,0,0),(0,255,0),(0,0,255)]
    for big,color in zip(biggies,bgr):
        cv2.drawContours(dupe,[big],-1,color,-1)
        #cv2.putText(frame,"X",tuple(temp[3]),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),thickness=2)
    cv2.addWeighted(dupe,opacity,frame,1-opacity,0,frame)
    cv2.drawContours(frame,_unrolled_corners(corners),-1,(0,0,0))

    #print type(biggies)

    cv2.drawContours(frame,[quad],-1,(0,0,0))

    return frame

def _extract_code(frame,refpoints,l):
    """Use the outermost corners of the QR
    code to fix perspective of the frame and
    cut out an image of the actual code.

    :frame: cv2 img
    :refpoints: list of four points
    :l: float, how long the sheared image should be
    :returns: cv2 img

    """
    #rows,cols,ch=frame.shape
    refpoints=np.float32(refpoints)

    #put the corners on the upper left
    newlocs=np.float32([[0,0],[l,0],[l,l],[0,l]])
    #M=cv2.getAffineTransform(refpoints,newlocs)
    M=cv2.getPerspectiveTransform(refpoints,newlocs)

    extracted=cv2.warpPerspective(frame,M,(l,l))

    return extracted

def extract_and_highlight(frame,l=100):
    """Highlight the corners in the frame and also
    cut out the code from the image.

    :frame: cv2 img
    :l: float, how long the sheared image should be
    :returns: cv2 img, cv2 img (highlighted frame and code)

    """
    framecopy=np.copy(frame)
    squares,hiersq=_squares(framecopy)
    corners=_corners(squares,unroll=False)
    biggies=_big_corners(corners)
    quad=_outer_quad(biggies)


    highlighted=_corner_highlight(framecopy,corners)
    extracted=np.zeros((l,l,3))

    if len(quad)==4:
        extracted=_extract_code(frame,quad,l)

    
    return highlighted,extracted
