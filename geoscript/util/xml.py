import sys
from javax.xml.namespace import QName
from util import doInput, doOutput
from org.geotools.xsd import Parser, Encoder, Configuration
from org.geotools.gml2 import GMLConfiguration as GML2
from org.geotools.gml3 import GMLConfiguration as GML3
from org.geotools.gml3.v3_2 import GMLConfiguration as GML32
from org.geotools.wfs.v1_0 import WFSConfiguration_1_0 as WFS10
from org.geotools.wfs.v1_1 import WFSConfiguration as WFS11
from org.geotools.wfs.v2_0 import WFSConfiguration as WFS20
from org.geotools.kml import KMLConfiguration as KML

def doParse(cls, xml, ver):
  return doInput(lambda input: Parser(cls.config(ver)).parse(input), xml)

def doEncode(cls, obj, el, ver, format, bounds, xmldecl, namespaces=True, 
             nsmappings={}, out=None):

  cfg = cls.config(ver)
  if not bounds:
    cfg.getProperties().add(GML2.NO_FEATURE_BOUNDS)

  e = Encoder(cfg)
  if not xmldecl:
    e.setOmitXMLDeclaration(True)
  if format:
    e.setIndenting(True)
  if namespaces:
    for pre,uri in nsmappings.iteritems():
      if uri:
        e.getNamespaces().declarePrefix(pre, uri)
  else:
    e.setNamespaceAware(False)

  if not isinstance(el, tuple):
    el = (cls.uri(ver), el) 

  qname = QName(el[0], el[1])
  
  if out:
    return doOutput(lambda output: e.encode(obj, qname, output), out)
  else:
    return e.encodeAsString(obj, qname)


class gml(object):

  @classmethod
  def uri(cls, ver):
    return (GML32() if ver == 3.2 else GML3()).getNamespaceURI()

  @classmethod
  def parse(cls, xml, ver):
    return doParse(cls, xml, ver)

  @classmethod
  def encode(cls, obj, el, ver, format, bounds, xmldecl, nsmappings={}, 
             out=None):
    return doEncode(cls, obj, el, ver, format, bounds, xmldecl, True, 
      nsmappings, out)
     
  @classmethod
  def config(cls, ver):
    return {
      2: lambda x: GML2(),
      3: lambda x: GML3(),
      3.2: lambda x: GML32()
    }[ver](0)

class wfs(object):

  @classmethod
  def uri(cls, ver):
    return (WFS20() if ver == 3.2 else WFS11()).getNamespaceURI()

  @classmethod
  def parse(cls, xml, ver):
    return doParse(cls, xml, ver)

  @classmethod
  def encode(cls, obj, el, ver, format, bounds, xmldecl, nsmappings={}, 
             out=None):
    return doEncode(cls, obj, el, ver, format, bounds, xmldecl, True, 
      nsmappings, out)

  @classmethod
  def config(cls, ver):
    return {
      2: lambda x: WFS10(),
      3: lambda x: WFS11(),
      3.2: lambda x: WFS20()
    }[ver](0)

class kml(object):

  @classmethod
  def uri(cls, ver):
    return KML().getNamespaceURI()

  @classmethod
  def parse(cls, xml):
    return doParse(cls, xml, None)

  @classmethod
  def encode(cls, obj, el, format, xmldecl, namespaces, out=None):
    return doEncode(cls, obj, el, None, format, True, xmldecl, namespaces, {}, 
      out)

  @classmethod
  def config(cls, ver):
    return KML()
