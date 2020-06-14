from geoscript import geom
from geoscript import viewer

bounds = geom.Bounds(-180,-90,180,90)
sierpinskiCarpet = geom.createSierpinskiCarpet(bounds, 50)
viewer.draw(sierpinskiCarpet)