import sys
from geoscript import util
from org.geotools.xml.styling import SLDTransformer

def writeSLD(style, out=sys.stdout, format=True):
  tx = SLDTransformer()
  if format: 
    tx.setIndentation(2)

  def write(os):
    tx.transform(style._style(), os) 

  util.doOutput(write, out)
