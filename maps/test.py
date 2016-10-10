from maps import *
from google import *



url=base_google_maps_api_url()
print url

coords=(34.417552,-119.853578)

url=append_generic_parameter(url,"center",[coord_to_str(coords)])
print url

url=append_generic_parameters(url,zoom=[50],size=["500x500"])
print url

print generate_generic_url(center=[coord_to_str(coords)],zoom=[50],size=["500x500"])

url=append_generic_parameters(url,markers=[coord_to_str(coords)])
print url

print chain_parameter_values([1,2,3,4,5,6])


multicoord=obfuscate_location(coords,(0.0042,0.0042),3)

zoomcoord=[]
for c in multicoord:
    zoomcoord+=(obfuscate_location(c,(0.0012,0.0012),2))
multicoord+=zoomcoord

for c in multicoord:
    zoomcoord+=(obfuscate_location(c,(0.00007,0.00007),2))
multicoord+=zoomcoord

print zoomcoord

print generate_generic_url(visible=coords_to_str(multicoord),markers=coords_to_str(multicoord),size=["1000x1000"])

testmap=GenericMap(coords,(0.0042,0.0042),5)
print testmap.obfuscated_url()

testtree=EasyMapTree(coords)
print testtree.focus_urls()[0][0]
print testtree.center_urls()[0]
print testtree.top_url()

#Resolution zoom size=1000x1000
#0.0012 18
#0.0006 19
#0.0003 20
#0.0001 21
#0.00007 22
