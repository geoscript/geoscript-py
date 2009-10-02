import example

from geoscript import style
from geoscript.map import Map
from geoscript.layer import ShapefileLayer

shp = ShapefileLayer('../tests/data/states.shp')
shp.style = style.parseSLD('../tests/data/states.sld')

map = Map()
map.add(shp)
map.render(antialias=False)
