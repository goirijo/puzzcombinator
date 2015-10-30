import importlib
import R4
import image

class Encoder(object):

    """Holds both the encoded message on a grid, as well
    as the decoder needed to read it."""

    def __init__(self,message,label,sym="R4"):
        """Automatically generate grids

        :message: string
        :label: string (for svg files)
        :sym: string, determines symmetry of grid

        """
        self._message = message
        self._label = label

        symmodule=importlib.import_module("puzzcombinator.encoder."+sym)
        self._decoder=symmodule.make(message)
        self._traced=symmodule.trace(message,self._decoder)

        self._gridpath=label+"_grid.svg"
        self._decoderpath=label+"_decoder.svg"
        self._encodedpath=label+"_encoded.svg"

        return

    def draw(self, target):
        """Write all the svg files to the target directory

        :target: string
        :returns: void

        """
        cr=image.draw_grid(target+"/"+self._gridpath,self._decoder)
        cr=image.draw_decoder(target+"/"+self._decoderpath,self._decoder)
        cr=image.draw_encoded(target+"/"+self._encodedpath,self._traced)

        return
