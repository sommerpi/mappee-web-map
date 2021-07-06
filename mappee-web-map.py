import folium
import pandas

# load volcanoes data
DATA = pandas.read_csv("volcanoes.txt")
LAT = list(DATA["LAT"])
LON = list(DATA["LON"])
ELEV = list(DATA["ELEV"])
NAME = list(DATA["NAME"])

# create map
MAP = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="Stamen Terrain")

# produce colour based on elevation
def color_producer(elevation):
  if elevation < 1000:
    return 'green'
  elif 1000 <= elevation < 3000:
    return 'orange'
  else:
    return 'red'

# add a feature group of volcanoes
def map_volcanoes():
  html = """
  Volcano name:<br>
  <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
  Height: %s m
  """
  fgv = folium.FeatureGroup(name="Volcanoes")

  for lt, ln, el, nm in zip(LAT, LON, ELEV, NAME):
    iframe = folium.IFrame(html=html % (nm, nm, str(el)), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe, parse_html=True), radius=6, fill_color=color_producer(el), color="grey", fill_opacity=0.7))
  return fgv

# add a feature group of population
def map_population():
  fgp = folium.FeatureGroup(name="Population")

  fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
  style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
  else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))
  return fgp

# add layer control
def layer_control(*args):
  for fg in args:
    MAP.add_child(fg)
  MAP.add_child(folium.LayerControl())

def main():
  fg_volcanoes = map_volcanoes()
  fg_population = map_population()
  layer_control(fg_volcanoes, fg_population)
  MAP.save("map_html_advanced.html")  # save the html page

if __name__ == '__main__':
  main()