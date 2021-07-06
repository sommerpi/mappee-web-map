import folium
import pandas

data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(elevation):
  if elevation < 1000:
    return 'green'
  elif 1000 <= elevation < 3000:
    return 'orange'
  else:
    return 'red'

map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="Stamen Terrain")

# add a feature group of volcanoes
fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el, nm in zip(lat, lon, elev, name):
  iframe = folium.IFrame(html=html % (nm, nm, str(el)), width=200, height=100)
  fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe, parse_html=True), radius=6, fill_color=color_producer(el), color="grey", fill_opacity=0.7))

# add a feature group of population
fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

# add layer control
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("map_html_advanced.html")