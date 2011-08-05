from java.util import Map
from geoscript.util import xml
from geoscript.feature.feature import Feature

def writeGML(f, ver=2, format=True, bounds=False, xmldecl=False, nsprefix='gsf'):
  """
  Writes a :class:`Feature <geoscript.feature.Feature>` object as GML.

  *ver* specifies the gml version to encode. Supported versions include 2, 3, 
  and 3.2.

  *format* specifies whether to format or pretty print the result.
  
  *bounds* specifies whether to include feature bounds in the result.

  *xmldecl* specifies whether to include the XML declaration in the result. 

  *nsprefix* specifies the prefix to be mapped to the namespace :attr:`uri <geoscript.feature.schema.Schema.uri>` for the feature schema. 
  """
  el = (xml.gml.uri(ver), "_Feature" if ver < 3.2 else "AbstractFeature")
  return xml.gml.encode(f._feature, el, ver, format, bounds, xmldecl, 
    {nsprefix: f.schema.uri})

def readGML(input, ver=2):
  """
  Reads a :class:`Feature <geoscript.feature.Feature>` from GML. 

  *input* is the GML to read specified as a str, file, or some other input 
  stream.

  *ver* specifies the gml version to encode. Supported versions include 2, 3, 
  and 3.2.
  """
  obj = xml.gml.parse(input, ver)
  if isinstance(obj, Map):
    # turn map into feature
    fid = obj.remove('fid')
    if not fid:
      fid = obj.remove('id')
    
    obj = Feature(dict(obj), fid)
  return obj
