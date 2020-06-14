import os, json
import folium
import pandas as pd

# read csv
df = pd.read_csv('data/coordinates/gensan_coords.csv')
path_to_json = 'geojson/gensan/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
#print(json_files)

psgc_code = list(df['psgc_code'])
province = list(df['province'])
address = list(df['formatted_address'])
lat = list(df['latitude'])
lon = list(df['longitude'])

html = """Location <br>
PSGC: %s <br>
Name: %s 
"""

def color_picker(province):
    u_province = list(df['province'].unique())
    #print(u_province)
    if province == u_province[1]:
        return "blue"
    """elif province == u_province[2]:
        return "red"
    elif province == u_province[3]:
        return "green" """



my_map = folium.Map(location=[7.3041622, 126.0893406], zoom_start = 10)
fg = folium.FeatureGroup(name = "Coordinates")
for lt, ln, add, code, prov in zip(lat,lon, address, psgc_code,province):
    iframe = folium.IFrame(html=html % (str(code), str(add)), width=200, height=100)
    fg.add_child(folium.CircleMarker(location=[lt,ln], radius = 7,popup=folium.Popup(iframe),
    fill_color = color_picker(prov), color = 'grey', fill = True, fill_opacity = 0.8))

fgb = folium.FeatureGroup(name = "Barangay")
for json_file in json_files:
    fgb.add_child(folium.GeoJson(data=open(path_to_json+'{}'.format(json_file), 'r', encoding='utf-8-sig').read()))

fgod = folium.FeatureGroup(name = "OD Matrix")
points = ([6.1071155, 125.149901],[6.2275973,125.1378792])
fgod.add_child(folium.PolyLine(points, color="red", weight=2.5, opacity=1))

## Next tasks: 
# Add line origin-destination
# Add chloropeth (to divide region into separate barangays, check geocode if they have shape)
my_map.add_child(fgb)
my_map.add_child(fg)
my_map.add_child(fgod)
my_map.save("webmap/Map1.html")