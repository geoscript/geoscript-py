import sys
from org.geotools.styling import SLDTransformer

def writeSLD(style, format=True):
  tx = SLDTransformer()
  if format: 
    tx.setIndentation(2)
  tx.transform(style, sys.stdout)
  
