#Used Folium Framework to map out data 

import requests 
import json
import pandas as pd
import folium
import random
import re
map = folium.Map(location=[40.689062620279174, -73.97674304620634], zoom_start=6, tiles="OpenStreetMap")
fg = folium.FeatureGroup(name="Trees", show = False)
fg2 = folium.FeatureGroup(name= "Parks", show = False)
fg3 = folium.FeatureGroup(name= "Squirrels In Central Park", show = False)
fg4 = folium.FeatureGroup(name = "Rats", show = False)
fg5 = folium.FeatureGroup(name = "Reported Green House Gas Emissions", show  = False)
fg6 = folium.FeatureGroup(name = "Healthy Certfied Stores", show = False)
fg7 = folium.FeatureGroup(name = "Botanical Gardens", show = False)
fg8 = folium.FeatureGroup(name = "Recycling Bins", show = False)
fg9 = folium.FeatureGroup(name = "Water Foutains", show = False)

map.add_child(fg)
map.add_child(fg2)
map.add_child(fg3)
map.add_child(fg4)
map.add_child(fg5)
map.add_child(fg6)
map.add_child(fg7)
map.add_child(fg8)
map.add_child(fg9)

squirrel_data = requests.get("https://data.cityofnewyork.us/resource/vfnx-vebw.json")
squirrel_data = squirrel_data.json()
squirrel_frame = pd.DataFrame(data= squirrel_data)
Squirrel_Lat = squirrel_frame["x"]
Squirrel_Lon = squirrel_frame["y"]

#geo json api for park
park_data = requests.get("https://data.cityofnewyork.us/resource/enfh-gkve.geojson")
park_data = park_data.json()
park_geojson = park_data
#regular json for park
park_data1 = requests.get("https://data.cityofnewyork.us/resource/enfh-gkve.json")
park_data1 = park_data1.json()

tree_data = requests.get("https://data.cityofnewyork.us/resource/uvpi-gqnh.json")
tree_data = tree_data.json()
tree_frame = pd.DataFrame(data=tree_data)

rat_data = requests.get("https://data.cityofnewyork.us/resource/p937-wjvj.json")
rat_data = rat_data.json()

energy_data = requests.get("https://data.cityofnewyork.us/resource/rgfe-8y2z.json")
energy_data = energy_data.json()

healthy_stores = requests.get("https://data.cityofnewyork.us/resource/ud4g-9x9z.json")
healthy_stores = healthy_stores.json()

Tree_Lat = tree_frame["latitude"]
Tree_Lon = tree_frame["longitude"]
Tree_Address = tree_frame["address"]
Tree_Health = tree_frame["health"]

botaincal_gardens = pd.read_csv("botaincal_gardens.csv")

water_fountain = requests.get("https://data.cityofnewyork.us/api/views/bevm-apmm/rows.json?accessType=DOWNLOAD")
water_fountain = water_fountain.json()
water_fountain1 = water_fountain["data"]

recycle_bins = requests.get("https://data.cityofnewyork.us/resource/sxx4-xhzg.json")
recycle_bins  = recycle_bins.json()
for y in water_fountain1:
    try:
        x = re.findall("\d+\.\d+",y[9])
        x = (x[1], "-" + x[0])
        fg9.add_child(folium.Marker(location = x, popup="Water Foutain", icon = folium.Icon(color = "darkpurple")))
    except:
        pass
for x in recycle_bins:
    try:
        fg8.add_child(folium.Marker(location = [x["latitude"], x["longitude"]], 
        popup= "Address: " + x["address"] + "\n Playground Name: " + x["park_site_name"], 
        icon = folium.Icon(color = "cadetblue")))
    except:
        pass
for x in botaincal_gardens.itertuples(): #we have to use .itertuples function because this is a csv file to index we need to use this. (prevoius )
    fg7.add_child(folium.Marker(location = [x.latitude, x.longitude], popup = x.name + "\n" + x.address, 
    icon = folium.Icon(color = "darkgreen")))

fg2.add_child(folium.GeoJson(park_geojson, name = "Parks",tooltip="Park", style_function= lambda x: {'fillColor': '#3E9940'}))
for c in healthy_stores:
    #using try and except because some of the values in the api is blank
    try:
        fg6.add_child(folium.Marker(location = [c["latitude"], c["longitude"]],
        popup ="Address: "+ c["street_address"]+ "\n Store Name: "+ c["store_name"],
        icon = folium.Icon(color = "lightblue")))
    except:
        pass
for y in energy_data:
    try:
        fg5.add_child(folium.Marker(location = [y["latitude"], y["longitude"]],
         popup="Total Green House Gas Emissions: \n"+ y["total_ghg_emissions_mtco2e"], 
         icon = folium.Icon(color = "orange")))
    except:
        pass
for x in rat_data:
    try:
        fg4.add_child(folium.Marker(location = [x["latitude"], x["longitude"]],
         popup = "Rat",
         icon = folium.Icon(color = "lightgray")))
    except:
        pass
for lt, ln, ad, hl in zip(Tree_Lat, Tree_Lon,Tree_Address, Tree_Health):    
    fg.add_child(folium.Marker(location=[lt, ln],
     popup="Tree" + ad + "\n" + "Condition: " + str(hl),
     icon=folium.Icon(color="green")))
for lat, lon in zip(Squirrel_Lat,Squirrel_Lon):
    fg3.add_child(folium.Marker(location=[lon, lat],
     popup="Squirrel",
     icon=folium.Icon(color="lightred")))
    #note only doing lon and lat in opposite order because the order is messed up on api response 
map.add_child(folium.LayerControl(position="topright"))
map.save("reForest_data.html")
