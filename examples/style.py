import example

from java import awt
from geoscript import map, style
from geoscript.layer import ShapefileLayer

s = style.polygon()
s.symbolizer().stroke = awt.Color.BLUE
s.symbolizer().width = 3
s.symbolizer().fill = awt.Color.GRAY

shp = ShapefileLayer('../tests/data/states.shp')
shp.style = s

map = map.Map()
map.add(shp)
map.render()
