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

def chain_parameter_values(values):
    """Create a URL chunk by concatenating a list of values
    with the '|' character

    :values: list
    :returns: str

    """
    urlchunk=str(values[0])

    for p in values[1::]:
        urlchunk+="|"
        urlchunk+=str(p)

    return urlchunk

def append_generic_parameter(apiurl,prameter,values):
    """Add the specified parameter to the URL

    :prameter: str
    :values: list str
    :returns: str

    """
    if values is not None:
        apiurl=prepare_url_for_new_parameter(apiurl)
        apiurl=apiurl+prameter+"="+chain_parameter_values(values)

    return apiurl

def append_generic_parameters(apiurl,**kwargs):
    """For every parameter specified, add it to
    the URL

    :apiurl: str
    :**kwargs: dict of list str
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

