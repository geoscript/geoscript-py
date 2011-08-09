import sys
from org.geotools.geojson.feature import FeatureJSON
from geoscript.util import doOutput, doInput
from geoscript.layer.cursor import Cursor

_fjson = FeatureJSON()

def writeJSON(obj, output=sys.stdout):
  """
  Writes a :class:`Layer <geoscript.layer.layer.Layer>` object as GeoJSON. This 
  method also accepts a :class:`Cursor <geoscript.layer.cursor.Cursor>`. 

  *output* specifies what to write the JSON to, a file or some other output stream.

  >>> import os
  >>> from geoscript.layer import Layer
  >>> from geoscript.geom import Point
  >>> 
  >>> l = Layer()
  >>> l.add([Point(1,2)])
  >>> l.add([Point(3,4)])
  >>> 
  >>> out = file(os.devnull, 'w')
  >>> writeJSON(l, output=out)
  >>> writeJSON(l.cursor('INTERSECTS(geom, POINT (1 2))'), output=out)
  """
  
  fcol = obj._fcol if isinstance(obj,Cursor) else obj._source.getFeatures()
  return doOutput(lambda out: _fjson.writeFeatureCollection(fcol, out), output)

def readJSON(json):
  """
  Reads a :class:`Layer <geoscript.layer.layer.Layer>` from GML. 

  *input* is the GML to read specified as a str, file, or some other input 
  stream.

  *ver* specifies the gml version to encode. Supported versions include 2, 3, 

  >>> json = '{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[1,2]},"properties":{},"id":"fid"}]}'
  >>> l = readJSON(json)
  >>> l.count()
  1
  """
  fcol = doInput(lambda input: _fjson.readFeatureCollection(input), json)

  from geoscript.workspace import Workspace
  ws = Workspace()
  ws._store.addFeatures(fcol)

  return [ws[name] for name in ws.layers()][0]
