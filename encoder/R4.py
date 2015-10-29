import numpy as np
import math
import random

def trace(secretmessage,grid):
    """Run through the grid and place a letter for each
    True slot as you go, rotating up to four times until
    you run out of space.
    """

    messagegrid=np.zeros(grid.shape,dtype=str)
    messagegrid[:,:]=" "
    dim=grid.shape[0]
    for rot in range(4):
        for y in range(dim):
            for x in range(dim):
                if grid[(x,y)]==True:
                    messagegrid[(x,y)]=secretmessage[0]
                    secretmessage=secretmessage[1::]
                    if len(secretmessage)==0:
                        return messagegrid
        grid=np.rot90(grid)

def template(messagestring):
    """Create a grid of appropriate dimensions to fit
    the given message and set all slots to False.
    If dimensions are odd, set the center tile to True,
    since that tile should be inaccessible.

    :messagestring: string
    :returns: ndarray of bool

    """
    numchars=len(messagestring)
    dim=int(math.ceil(math.sqrt(numchars)))
    
    #check if dimensions are odd. If removing the center tile makes
    #the grid too small, add an extra tile to the dimensions
    if dim%2!=0 and (dim*dim-1)<numchars:
        dim+=1

    grid=np.zeros((dim,dim),dtype=bool)
    if dim%2!=0:
        grid[dim/2,dim/2]=True
    return grid

def make(messagestring):
    """Create an decoder that reveals the given message
    with 4 90 degree rotations.

    :messagestring: string
    :returns: ndarray of bool

    """
    counter=template(messagestring)
    grid=np.copy(counter)
    grid[...]=False

    while not np.all(counter==True):
        candidates=np.where(counter==False)
        candidates=zip(candidates[0],candidates[1])
        winind=random.randint(0,len(candidates)-1)
        winner=candidates[winind]

        grid[winner]=True

        for rot in range(4):
            counter=np.rot90(counter)
            counter[winner]=True

    return grid

