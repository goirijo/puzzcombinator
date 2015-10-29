import numpy as np
import cairo

def _canvas_dims(decoder,ts):
    """TODO: Docstring for _canvas_dims.

    :decoder: ndarray
    :ts: int, size of a square tile
    :returns: (int,int,int,int) width and height of canvas; tiles in x and y directions

    """
    xtiles,ytiles=decoder.shape
    w=xtiles*ts+2*ts
    h=ytiles*ts+2*ts
    
    return (w,h,xtiles,ytiles)

def _grid_canvas(target,decoder,ts,lw):
    """Create a cairo surface to draw on of the appropriate
    dimensions. Fits the appropriate number of tiles and
    has a one tile buffer around the edges.

    :target: svg filename
    :decoder: ndarray
    :ts: int, size of a square tile
    :lw: int, line width
    :returns: cairo context

    """
    w,h,xtiles,ytiles=_canvas_dims(decoder,ts)
    ps = cairo.SVGSurface(target, w, h)
    cr = cairo.Context(ps)

    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(lw)

    return cr

def _stroke_grid(cr,decoder,ts):
    """TODO: Docstring for _stroke_grid.

    :cr: cairo context
    :decoder: ndarray
    :ts: int, size of a square tile
    :returns: cairo context

    """
    w,h,xtiles,ytiles=_canvas_dims(decoder,ts)
    #draw vertical lines
    for x in range(xtiles+1):
        cr.move_to(x*ts+ts,ts)
        cr.line_to(x*ts+ts,h-ts)

    #draw horizontal lines
    for y in range(ytiles+1):
        cr.move_to(ts,y*ts+ts)
        cr.line_to(w-ts,y*ts+ts)
    
    cr.stroke()
    return cr

def _fill_corners(cr,decoder,ts):
    """Place decorations on corners of decoder
    to use as an orientation

    :cr: cairo context
    :decoder: ndarray
    :returns: cairo context

    """
    w,h,xtiles,ytiles=_canvas_dims(decoder,ts)

    cr.set_line_width(0)

    cr.rectangle(0,w-0.5*ts,0.5*ts,0.5*ts)

    cr.rectangle(w-0.5*ts,h-0.5*ts,0.5*ts,0.5*ts)
    cr.rectangle(w-ts,h-ts,0.5*ts,0.5*ts)

    cr.rectangle(w-0.5*ts,0,0.5*ts,0.5*ts)
    cr.rectangle(w-ts,0,0.5*ts,0.5*ts)
    cr.rectangle(w-0.5*ts,0.5*ts,0.5*ts,0.5*ts)

    cr.rectangle(0,0,ts,ts)

    cr.fill_preserve()

    return cr

def _block_tile(cr,ts,x,y):
    """Fill a single tile with index x,y of the encoder
    with black

    :cr: cairo context
    :ts: int, tile size
    :decoder: ndarray, dtype=bool
    :x: int
    :y: int
    :returns: cairo context

    """
    cr.set_line_width(0)
    cr.rectangle(ts*(x+1),ts*(y+1),ts,ts)
    cr.fill_preserve()
    
    return cr

def _stamp_tile(cr,ts,fs,lw,x,y,char):
    """Place a single character at the center of the
    specified x,y tile of the grid. 

    :cr: cairo context
    :ts: int, tile size
    :fs: float, font size relative to tile size
    :lw: int, line width
    :x: int
    :y: int
    :char: string, one letter
    :returns: cairo context

    """
    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
                    cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(fs*(ts-lw))

    pad=(1-fs)*ts/2.0+lw
    cr.move_to(ts*(x+1)+pad,ts*(y+2)-pad)
    cr.show_text(char)

    return cr

def draw_grid(target,decoder,ts=60,lw=6):
    """Create an svg image of a grid with the appropriate
    number of tiles. Includes a border.

    :target: svg filename
    :decoder: ndarray
    :ts: int, size of a square tile
    :fs: float, font size relative to tile size
    :lw: int, line width
    :returns: cairo context

    """
    cr=_grid_canvas(target,decoder,ts,lw)
    cr=_stroke_grid(cr,decoder,ts)
    cr=_fill_corners(cr,decoder,ts)

    return cr

def draw_decoder(target,decoder,ts=60,lw=6):
    """Create an svg image of the decoder, with the appropriate
    tiles blacked out. Includes a border.

    :target: svg filename
    :decoder: ndarray
    :ts: int, size of a square tile
    :lw: int, line width
    :returns: cairo context

    """
    cr=draw_grid(target,decoder,ts,lw)

    for xind, x in enumerate(decoder):
        for yind, y in enumerate(x):
            if not y:
                _block_tile(cr,ts,xind,yind)

    return cr

def draw_encoded(target,traced,message,ts=60,lw=6,fs=0.7):
    """Trace out the message onto the grid such that
    it can only be recovered with the decoder.

    :target: svg filename
    :traced: ndarray of string
    :message: string
    :ts: int, size of a square tile
    :lw: int, line width
    :returns: cairo context

    """
    cr=draw_grid(target,traced,ts,lw)

    for xind, x in enumerate(traced):
        for yind, y in enumerate(x):
            _stamp_tile(cr,ts,fs,lw,xind,yind,y)

    return cr

