import numpy as np
import statm2d as sm2d
import math
import random
import cairo

def trace_R4(secretmessage,grid):
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

def template_R4(messagestring):
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

def R4(messagestring):
    """Create an decoder that reveals the given message
    with 4 90 degree rotations.

    :messagestring: string
    :returns: ndarray of bool

    """
    counter=template_R4(messagestring)
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

def draw_decoder_grid(target,decoder,ts=60,fs=0.7,lw=6):
    """Create an svg image of a grid with the appropriate
    number of tiles. Includes a border.

    :target: svg filename
    :decoder: ndarray
    :ts: int, size of a square tile
    :fs: float, font size relative to tile size
    :lw: int, line width
    :returns: void

    """
    xtiles,ytiles=decoder.shape
    w=xtiles*ts+2*ts
    h=ytiles*ts+2*ts
    ps = cairo.SVGSurface(target, w, h)
    cr = cairo.Context(ps)
    
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(lw)
    
    #draw the edges of the decoder
    #cr.move_to(ts,ts)
    #cr.line_to(ts,h-ts)
    #cr.line_to(w-ts,h-ts)
    #cr.line_to(w-ts,ts)
    #cr.line_to(ts,ts)

    #draw vertical lines
    for x in range(xtiles+1):
        cr.move_to(x*ts+ts,ts)
        cr.line_to(x*ts+ts,h-ts)

    #draw horizontal lines
    for y in range(ytiles+1):
        cr.move_to(ts,y*ts+ts)
        cr.line_to(w-ts,y*ts+ts)

    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
                    cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(round(fs*ts))

    pad=(1-fs)*ts/2.0+lw/2.0
    cr.move_to(ts+pad,2*ts-pad)
    cr.show_text("H")

    cr.rectangle(3*ts,4*ts,ts,ts)
    cr.fill_preserve()

    cr.stroke()
    cr.show_page()
