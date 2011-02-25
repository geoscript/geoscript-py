import re
from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from org.geotools.styling import TextSymbolizer

_weights = ['normal', 'bold']
_styles = ['normal', 'italic', 'oblique']

class Font(Symbolizer):

  def __init__(self, font):
    Symbolizer.__init__(self)
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
    font = font.replace(', +', ',').strip(';')

    chunks = [''] 
    quote = False
    for c in font:
      if c == ' ' and not quote:
        chunks.append('')
      elif c == '"':
        quote = not quote
      else:
        chunks[-1] += c

    self.style = None 
    self.weight = None
    self.size = 10
    self.family = 'serif'

    for chunk in chunks:
      if not self.style and chunk in _styles:
        self.style = chunk
      elif not self.weight and chunk in _weights:
        self.weight = chunk
      else:
        m = re.search('\d+', chunk)
        if m:
          self.size = m.group(0)
        else:
          self.family = chunk

