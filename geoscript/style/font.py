import re
from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from org.geotools.styling import TextSymbolizer
from org.geotools.renderer.style import FontCache

_weights = ['normal', 'bold']
_styles = ['normal', 'italic', 'oblique']

class Font(Symbolizer):
  """
  Symbolizer for label font.

  A font consists of a ``style`` (normal, italic, or oblique), a ``weight`` 
  (normal or bold), a ``size``, and a font ``family``. A font can be constructed by
  specifying any number of these properties:

  >>> Font(style='italic', weight='bold', size=10, family='Arial')
  Font(style=italic,weight=bold,size=10,family=Arial)

  A font may also be constructed from a CSS like string that specifies the 
  attribute values in order.

  >>> Font('italic bold 12px "Times New Roman"')
  Font(style=italic,weight=bold,size=12,family=Times New Roman)

  If the font family contains spaces, it should be surrounded in quotes. Multiple
  values for font family may also be specified to form provide fallback values.

  >>> Font('"Times New Roman", Arial, serif')
  Font(style=normal,weight=normal,size=10,family=Times New Roman,Arial,serif)
  """

  @staticmethod
  def list():
    """
    Returns a generator of all available Font names.
    """
    for f in sorted(FontCache.getDefaultInstance().getAvailableFonts()):
      yield f
    
  def __init__(self, font=None, style='normal', weight='normal', size=10, 
               family='serif'):
    Symbolizer.__init__(self)
    
    self.style = style
    self.weight = weight
    self.size = size
    self.family = family

    if font:
      self._parse(font)

  def _prepare(self, syms):
    syms = util.symbolizers(syms, TextSymbolizer)
    for sym in syms:
      self._apply(sym)

  def _apply(self, sym):
    f = self.factory.createFont(self.family, self.style == "italic", 
      self.weight == "bold", float(self.size))
    sym.setFont(f)    

  def _parse(self, font):
    # font-style font-weight font-size font-family
    font = re.sub(', +', ',', font).strip(';')

    chunks = [''] 
    quote = False
    for c in font:
      if c == ' ' and not quote:
        chunks.append('')
      elif c == '"':
        quote = not quote
      else:
        chunks[-1] += c

    style = None 
    weight = None

    for chunk in chunks:
      if not style and chunk in _styles:
        style = chunk
      elif not weight and chunk in _weights:
        weight = chunk
      else:
        m = re.search('\d+', chunk)
        if m:
          self.size = m.group(0)
        else:
          self.family = chunk

    if style:
      self.style = style
    if weight:
      self.weight = weight

  def __repr__(self):
    return self._repr('style','weight','size','family')
