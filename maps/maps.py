#https://developers.google.com/maps/documentation/static-maps/intro

def base_google_maps_api_url():
    """Return string of the API URL without any
    of the parameters
    :returns: str

    """
    return "https://maps.googleapis.com/maps/api/staticmap?"

def prepare_url_for_new_parameter(apiurl):
    """If necessary, add '&' to the end of the URL.
    Call this whenever you plan on adding a new parameter.

    :apiurl: str
    :returns: str

    """
    #if not ending in '?' then it's not the first parameter
    if apiurl[-1]!='?':
        apiurl=apiurl+"&"

    return apiurl

def append_generic_parameter(apiurl,prameter,value):
    """Add the specified parameter to the URL

    :prameter: str
    :value: str
    :returns: str

    """
    apiurl=prepare_url_for_new_parameter(apiurl)
    apiurl=apiurl+prameter+"="+str(value)

    return apiurl

def append_generic_parameters(apiurl,**kwargs):
    """For every parameter specified, add it to
    the URL

    :apiurl: str
    :**kwargs: dict of str
    :returns: str

    """
    for kwarg in kwargs:
        apiurl=append_generic_parameter(apiurl,kwarg,kwargs[kwarg])

    return apiurl

def generate_generic_url(**kwargs):
    """Given some google API kwargs, generate
    the URL. This method is not smart.

    :**kwargs: dict of str
    :returns: str

    """
    apiurl=base_google_maps_api_url()
    return append_generic_parameters(apiurl,**kwargs)
