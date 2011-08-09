import sys
from net.opengis.wfs import WfsFactory
from geoscript.layer.cursor import Cursor
from geoscript.util import xml

def writeGML(obj, ver=2, format=True, bounds=False, xmldecl=False, 
             nsprefix='gsf', output=sys.stdout):
  """
  Writes a :class:`Layer <geoscript.layer.layer.Layer>` object as GML. This 
  method also accepts a :class:`Cursor <geoscript.layer.cursor.Cursor>`. 

  *ver* specifies the gml version to encode. Supported versions include 2, 3, 
  and 3.2.

  *format* specifies whether to format or pretty print the result.
  
  *bounds* specifies whether to include feature bounds in the result.

  *xmldecl* specifies whether to include the XML declaration in the result. 

  *nsprefix* specifies the prefix to be mapped to the namespace :attr:`uri <geoscript.feature.schema.Schema.uri>` for the feature schema. 

  *output* specifies what to write the GML to, a file or some other output stream.

  >>> import os
  >>> from geoscript.layer import Layer
  >>> from geoscript.geom import Point
  >>> 
  >>> l = Layer()
  >>> l.add([Point(1,2)])
  >>> l.add([Point(3,4)])
  >>> 
  >>> out = file(os.devnull, 'w')
  >>> writeGML(l, output=out)
  >>> writeGML(l.cursor('INTERSECTS(geom, POINT (1 2))'), output=out)
  """

  fc = WfsFactory.eINSTANCE.createFeatureCollectionType()

  l = obj
  if isinstance(obj, Cursor):
    l = obj.layer
    fc.feature.add(obj._fcol)
  else:
    fc.feature.add(obj._source.getFeatures())

  return xml.wfs.encode(fc, "FeatureCollection", ver, format, bounds, xmldecl, 
    {nsprefix: l.schema.uri}, output)

def readGML(input, ver=2):
  """
  Reads a :class:`Layer <geoscript.layer.layer.Layer>` from GML. 

  *input* is the GML to read specified as a str, file, or some other input 
  stream.

  *ver* specifies the gml version to encode. Supported versions include 2, 3, 

  >>> xml = '<wfs:FeatureCollection xmlns:gml="http://www.opengis.net/gml" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gsf="http://geoscript.org/feature"><gml:featureMember><gsf:layer_0 fid="fid"><gsf:geom><gml:Point><gml:coord><gml:X>1.0</gml:X><gml:Y>2.0</gml:Y></gml:coord></gml:Point></gsf:geom></gsf:layer_0></gml:featureMember></wfs:FeatureCollection>'
  >>> l = readGML(xml)
  >>> l.count()
  1
  """
  fc = xml.wfs.parse(input, ver)

  from geoscript.workspace import Workspace
  ws = Workspace()
  for f in fc.feature: 
    ws._store.addFeatures(f)

  layers = [ws[name] for name in ws.layers()]
  return layers if len(layers) > 1 else layers[0]
