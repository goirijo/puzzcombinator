from maps import *

url=base_google_maps_api_url()
print url

url=append_generic_parameter(url,"center","0.000,5.123")
print url

url=append_generic_parameters(url,zoom=50,size="500x500")
print url

print generate_generic_url(center="0.000,5.123",zoom=50,size="500x500")
