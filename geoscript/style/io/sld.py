import sys
from geoscript import util
from org.geotools.styling import SLDTransformer

def writeSLD(style, out=sys.stdout, format=True):
  tx = SLDTransformer()
  if format: 
    tx.setIndentation(2)

  out = util.toOutputStream(out)
  try:
    tx.transform(style, out)
  finally:
    if out and out.close:
       out.close()
  
