import os
from geoscript.workspace.ogr import OGR

class FGDB(OGR):
  def __init__(self, db):
    OGR.__init__(self, db)
