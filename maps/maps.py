import google
import random

def distributed_coordinates(anchor,ranges,amount):
    """Given a latitude and longitude, generate a specified
    amount of additional latitudes and longitudes that are
    within the specified relative range of the original ones.

    :anchor: (float,float)
    :ranges: (float,float)
    :amount: int
    :returns: list of (float,float)

    """
    anchorlat,anchorlong=anchor
    rangelat,rangelong=ranges

    maxlat=anchorlat+rangelat
    minlat=anchorlat-rangelat
    maxlong=anchorlong+rangelong
    minlong=anchorlong-rangelong

    fuzzlats=[random.uniform(maxlat,minlat) for i in range(amount)]
    fuzzlongs=[random.uniform(maxlong,minlong) for i in range(amount)]

    return zip(fuzzlats,fuzzlongs)

def obfuscate_location(location,ranges,amount):
    """Given a location, randomly pick an anchor that falls within
    the specified range and generate new coordinates around the new anchor.
    The result is a list of coordinates that is randomly centered
    and contains the original location somewhere.

    :location: (float,float)
    :ranges: (float,float)
    :amount: int
    :returns: list of (float,float)

    """
    anchor=distributed_coordinates(location,ranges,1)[0]

    new_coords=distributed_coordinates(anchor,ranges,amount)
    new_coords.append(location)

    random.shuffle(new_coords)
    return new_coords


def coord_to_str(latlong):
    """Convert a tuple of latitude and longitude into
    a string digestible by the maps API

    :latlong: (float,float)
    :returns: str

    """
    lat,lng=latlong
    return str(lat)+","+str(lng)

def coords_to_str(latlongs):
    """Convert a list of tuples of latitude and longitude into
    a list of strings digestible by the maps API

    :latlong: list of (float,float)
    :returns: list of str

    """
    return [coord_to_str(latlong) for latlong in latlongs]

def size_to_str(size):
    """Convert width,height tuple into a digestible string
    for the size parameter in the maps API

    :size: (int,int)
    :returns: str

    """
    width,height=size
    return str(width)+"x"+str(height)


class GenericMap(object):

    """Store basic information to generate a map tile that contains
    a secret location, obfuscated by an additional number of markers.
    Zoom level and image resolution are left to the user, which sadly
    can be picked in a stupid manner.
    """


    def __init__(self,location,obfuscation,repetition,size=(640,640),zoom=None,scale=None):
        """Store all relevant variables. The presumption is that you don't have an API
        key, so only free stuff (e.g. max size is 640x640).

        :location: (float,float)
        :obfuscation: (float,float)
        :repetition: int
        :zoom: int or None
        :size: (int,int)
        :scale: int

        """
        self._location = location
        self._obfuscation_values = obfuscation
        self._repetition = repetition
        self._size = size
        self._zoom = zoom
        self._scale = scale

        self._obfuscated_location=obfuscate_location(self._location,self._obfuscation_values,self._repetition)


    def obfuscated_location(self,asstring=True):
        """Returns a list of markers, transformed to strings
        (or not)

        :asstring: bool
        :returns: List of str

        """
        if asstring:
            return coords_to_str(self._obfuscated_location)
        else:
            return self._obfuscated_location


    def obfuscated_url(self):
        """Generate URL for the instantiated map with the real location
        as well as all the fake ones

        :returns: str

        """
        location_strs=coords_to_str(self._obfuscated_location)
        size_str=size_to_str(self._size)

        return google.generate_generic_url(visble=location_strs,
                markers=location_strs,
                zoom=[self._zoom],size=[size_str])
        
    def location_url(self,location=None):
        """Generate URL for the instantiated map with only the real location
        or the fake one of the given index.

        :index: int
        :returns: str

        """
        obfs_strs=coords_to_str(self._obfuscated_location)
        size_str=size_to_str(self._size)
        location_str=""

        if location is None:
            location_str=coord_to_str(self._location)
        else:
            location_str=coord_to_str(location)

        return google.generate_generic_url(visble=obfs_strs,
                markers=[location_str],
                zoom=[self._zoom],size=[size_str])

    def all_location_urls(self):
        """Calls location_url for everything
        :returns: TODO

        """
        print [self.location_url(l) for l in self._obfuscated_location]
        return [self.location_url(l) for l in self._obfuscated_location]
        

class EasyMapTree(object):

    """Holds a secret latitude and longitude, whose precise value
    is obfuscated by several zoom levels of maps. This map provides
    URLs to Google maps that give different levels of information of
    where the specified latitude and longitude are.
    
    For now this class is going to be very rigid. You only get to specify
    the secret location and the levels of obfuscation (how many additional
    locations to hide the real one among). The zoom levels, amount of scatter
    in the dummy locations, etc are all predetermined.
    
    The map tree has stages:
    *Outermost zoom, with a few clouds of locations
    *One cloud of locations (zoomed up)
    *Singe marker
    """

    def __init__(self,location):
        """
        Comes up with a tree of GenericMaps for a specified location.
        Zoom levels, number of markers, etc. all picked automatically.

        :location: (float,float)

        """
        self._location = location
        
        self._topmap=GenericMap(location,(0.0042,0.0042),5)
        self._topmap.obfuscated_location()
        self._centermaps=[GenericMap(c,(0.0001,0.0001),6,zoom=21) 
                for c in self._topmap.obfuscated_location(asstring=False)]

        self._topmap._obfuscated_location=[loc for cm in self._centermaps for loc in cm._obfuscated_location]



    def top_url(self):
        """Gets the URL for the top level view with everything.

        :returns: str

        """
        return self._topmap.obfuscated_url()
    
    def center_urls(self):
        """Get all the URLs for the center tiles. These sill contain
        several markers.

        :returns: list of str
        """
        return [centermap.obfuscated_url() for centermap in self._centermaps]

    def focus_urls(self):
        """Get all the URLs, one for each marker. Each URL displays
        only one marker

        :returns: list if list of str
        """
        return [ centergroup for centergroup in [ zoommap.all_location_urls() for zoommap in self._centermaps ] ]

