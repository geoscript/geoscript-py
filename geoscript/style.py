from java import awt
from java import lang
from geoscript import util
from geoscript.filter import Filter
from org.geotools.filter import FilterFactoryImpl
from org.geotools.styling import StyleBuilder, SLDParser, UserLayer
from org.geotools.styling import Style as _Style
from org.geotools.styling import PointSymbolizer  as _PointSymbolizer
from org.geotools.styling import LineSymbolizer  as _LineSymbolizer
from org.geotools.styling import PolygonSymbolizer as _PolygonSymbolizer
 
_sb = StyleBuilder()
 
def point():
  sym = _sb.createPointSymbolizer()
  return Style(_sb.createStyle(sym))
 
def line():
  sym = _sb.createLineSymbolizer()
  return Style(_sb.createStyle(sym))
 
def polygon():
  sym = _sb.createPolygonSymbolizer()
  return Style(_sb.createStyle(sym))
 
def parseSLD(file):
   """
   Constructs a style from a StyledLayerDescriptor (SLD) file.
 
   >>> s = parseSLD('tests/data/states.sld')
   >>> len(s.rules())
   4
   """
   url = util.toURL(file)
   if url: 
     parser = SLDParser(_sb.styleFactory)
     parser.setInput(url.getFile())
     sld = parser.parseSLD() 
 
     if len(sld.styledLayers) > 0:
       sl = sld.styledLayers[0]
       if isinstance(sl,UserLayer):
         return Style(sl.getUserStyles()[0]) if len(sl.getUserStyles()) > 0 else None
       elif len(sl.getStyles()) > 0:
         return Style(sl.getStyles()[0])
 
class Style(object):
   """ 
   A style defines the portrayal of a layer.
 
   """ 
 
   def __init__(self, style=_sb.createStyle()): 
      self.style = style
      
   def rules(self):  
      rules = []
      for r in self.style.getFeatureTypeStyles()[0].getRules():
         rules.append(Rule(rule=r))
 
      return rules
 
   def rule(self):
      rules = self.rules()
      if len(rules) > 0:
        return rules[0]
 
   def symbolizers(self):
      syms = []
      for r in self.rules():
        syms.extend(r.symbolizers())
 
      return syms
 
   def symbolizer(self):
      rule = self.rule()
      if rule:
        return rule.symbolizer()
 
class SLD(Style):
 
   def __init__(self, sld):
     Style.__init__(self, parseSLD(sld))
 
class Rule(object):
   """
   A rule is a set of symbolizers, and an optional filter.
 
   >>> from java.awt import Color
   >>> from geoscript import filter
   >>> rule = Rule([PointSymbolizer(Color(75,100,125), 2)], filter.fromCQL("NAME= 'foo'"))
   >>> str(rule)
   'Rule(symbolizers=[Point(color=rgb(75,100,125), size=2)], filter=[ NAME = foo ])'
   """   
 
   def __init__(self, syms=[], fil=Filter.PASS, rule=None):
      self.rule = rule if rule else _sb.createRule([])
       
      fil = Filter(fil)
      if fil:
        self.rule.filter = fil
    
      if len(syms) > 0:
        self.rule.setSymbolizers([s.sym for s in syms])
 
   def symbolizers(self):
      syms = []
 
      for s in self.rule.getSymbolizers():
        sym = None
        if isinstance(s, _PointSymbolizer):
           sym = PointSymbolizer(sym=s)
        elif isinstance(s, _LineSymbolizer):
           sym = LineSymbolizer(sym=s) 
        elif isinstance(s, _PolygonSymbolizer): 
           sym = PolygonSymbolizer(sym=s) 
 
        if sym:
          syms.append(sym) 
       
      return syms
 
   def symbolizer(self):
      syms = self.symbolizers()
      if len(syms) > 0:
        return syms[0]
 
   def __str__(self):
      string = ','.join([str(sym) for sym in self.symbolizers()])
      return 'Rule(symbolizers=[%s], filter=%s)' % (string, self.rule.filter)
 
def cstr(color):
  return 'rgb(%d,%d,%d)' % (color.red,color.green,color.blue)
 
class Symbolizer(object):
   """
   Base class for symbolizers.
   """
 
   def __init__(self,sym):
      self.sym = sym
 
class PointSymbolizer(Symbolizer):
   """
   Symbolizer for Point geometries.
 
   >>> from java.awt import Color
   >>> sym = PointSymbolizer(Color(100,250,75), 3)
   >>> str(sym)
   'Point(color=rgb(100,250,75), size=3)'
   """
 
   def __init__(self, color=None, size=None, sym=_sb.createPointSymbolizer()):
      if not sym.graphic:
        sym.graphic = _sb.createGraphic()
 
      if len(sym.graphic.getMarks()) == 0:
        sym.graphic.addMark(_sb.createMark())
 
      m = sym.graphic.getMarks()[0]
      m.fill = m.fill if m.fill else _sb.createFill()
 
      if color:
        m.fill.color = _sb.literalExpression(color) 
 
      if size:
        m.setSize(_sb.literalExpression(size))
 
      Symbolizer.__init__(self,sym)
 
   def getcolor(self):
     return self._mark().fill.color.evaluate(None, awt.Color)
 
   def setcolor(self, color):
     self._mark().fill.color = _sb.literalExpression(color) 
 
   color = property(getcolor, setcolor)
 
   def getsize(self):
      return self._mark().size.evaluate(None, lang.Integer)
 
   def setsize(self, size):
     self._mark().size = _sb.literalExpression(size)
 
   size = property(getsize, setsize)
 
   def _mark(self):
      g = self.sym.graphic
      if g:
         if len(g.marks) > 0:
           return g.marks[0]
                  
   def __str__(self):
      return 'Point(color=%s, size=%d)' % (cstr(self.color), self.size)
 
 
class LineSymbolizer(Symbolizer):
   """
   Symbolizer for LineString geometries.
 
   >>> from java.awt import Color
   >>> sym = LineSymbolizer(Color(50,200,100), 4)
   >>> str(sym)
   'Line(color=rgb(50,200,100), width=4)'
   """
 
   def __init__(self, color=None, width=None, sym=_sb.createLineSymbolizer()):
      if not sym.stroke:
        sym.stroke = _sb.createStroke()
 
      if color:
        sym.stroke.color = _sb.literalExpression(color)
 
      if width:
        sym.stroke.width = _sb.literalExpression(width)
 
      Symbolizer.__init__(self,sym)
 
   def getcolor(self):
      return self.sym.stroke.color.evaluate(None,awt.Color) 
 
   def setcolor(self, color):
      self.sym.stroke.color = _sb.literalExpression(color)
      
   color = property(getcolor, setcolor)
 
   def getwidth(self):
      return self.sym.stroke.width.evaluate(None,lang.Integer)
 
   def setwidth(self, width):
      self.sym.stroke.width = _sb.literalExpression(width)
 
   width = property(getwidth, setwidth)
 
   def __str__(self):
     return 'Line(color=%s, width=%d)' % (cstr(self.color), self.width)
 
class PolygonSymbolizer(Symbolizer):
   """
   Symbolizer for Polygon geometries.
 
   >>> from java.awt import Color
   >>> sym = PolygonSymbolizer(Color(100,255,100), 5, Color(200,155,200))
   >>> str(sym)
   'Polygon(stroke=rgb(100,255,100), width=5, fill=rgb(200,155,200))'
   """
 
   def __init__(self, stroke=None, width=None, fill=None, sym=_sb.createPolygonSymbolizer()):
      if not sym.stroke:
        sym.stroke = _sb.createStroke()
 
      if not sym.fill:
        sym.fill = _sb.createFill()
 
      if stroke:
        sym.setStroke(_sb.createStroke(stroke))
      if width: 
        sym.stroke.width = _sb.literalExpression(width)
      if fill:
        sym.fill = _sb.createFill(fill)
 
      Symbolizer.__init__(self,sym)
     
   def getstroke(self):
      return self.sym.stroke.color.evaluate(None,awt.Color)
 
   def setstroke(self, color):
      self.sym.stroke.color = _sb.literalExpression(color)
 
   stroke = property(getstroke, setstroke)
 
   def getwidth(self):
      return self.sym.stroke.width.evaluate(None,lang.Integer)
 
   def setwidth(self, width):
      self.sym.stroke.width = _sb.literalExpression(width)      
 
   width = property(getwidth, setwidth)
 
   def getfill(self):
      return self.sym.fill.color.evaluate(None,awt.Color)
  
   def setfill(self, color):
      self.sym.fill.color = _sb.literalExpression(color)
 
   fill = property(getfill, setfill)
 
   def __str__(self):
      return 'Polygon(stroke=%s, width=%d, fill=%s)' % (cstr(self.stroke), self.width, cstr(self.fill))
 
