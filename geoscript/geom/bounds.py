from org.geotools.geometry import GeneralEnvelope
from org.geotools.geometry.jts import ReferencedEnvelope
from geoscript.util import deprecated
from geoscript import core, proj

class Bounds(ReferencedEnvelope):
  """
  A two dimensional bounding box.
  """
  def __init__(self, west=None, south=None, east=None, north=None, prj=None, env=None):
    if prj:
      prj = proj.Projection(prj)

    if env:
      if isinstance(env, GeneralEnvelope):
        env = ReferencedEnvelope(env)

      if prj:
        ReferencedEnvelope.__init__(self, env, prj._crs)
      elif hasattr(env, 'crs') and env.crs():
        ReferencedEnvelope.__init__(self, env, env.crs())
      else:
        ReferencedEnvelope.__init__(self, env, None)
    else:
      if west != None:
        ReferencedEnvelope.__init__(self, west, east, south, north, 
           prj._crs if prj else None)
      elif prj:
        ReferencedEnvelope.__init__(self, prj._crs) 
      else:
        ReferencedEnvelope.__init__(self)

  def getwest(self):
    return self.minX()
  west = property(getwest,None,None,'The leftmost/westmost oordinate of the bounds.')
  

  @deprecated
  def get_l(self):
    return self.west
  l = property(get_l, None, None, "Use west.")

  def getsouth(self):
    return self.minY()
  south = property(getsouth,None,None,'The bottomtmost/southmost oordinate of the bounds.')

  @deprecated
  def get_b(self):
    return self.south
  b = property(get_b, None, None, "Use south.")

  def geteast(self):
    return self.maxX()
  east = property(geteast,None,None,'The rightmost/eastmost oordinate of the bounds.')

  @deprecated
  def get_r(self):
    return self.east
  r = property(get_r, None, None, 'Use east.')

  def getnorth(self):
    return self.maxY()
  north = property(getnorth,None,None,'The topmost/northmost oordinate of the bounds.')

  @deprecated
  def get_t(self):
    return self.north
  t = property(get_t, None, None, 'Use north.')

  def getproj(self):
    crs = self.coordinateReferenceSystem
    if crs:
      return proj.Projection(crs)
  proj = property(getproj,None,None,'The :class:`Projection <geoscript.proj.Projection>` of the bounds. ``None`` if the projection is unknown.')

  def get_aspect(self):
    return self.width / self.height 
  aspect = property(get_aspect,None,None,'Ratio of width to height for this bounds.')

  def reproject(self, prj):
    """
    Reprojects the bounding box.
    
    *prj* is the destination :class:`Projection <geoscript.proj.Projection>` 

    """
    if not self.proj:
      raise Exception('No projection set on bounds, unable to reproject')

    prj = proj.Projection(prj)
    return Bounds(env=self.transform(prj._crs, True), prj=prj)

  def scale(self, factor):
    """
    Scales the bounds by a specified factor.

    *factor* is the scale factor. The scale factor must be greather than 0. A 
    value greater than 1 will grow the bounds whereas a value of less than 1 
    will shrink the bounds.
   
    This method returns a new :class:`Bounds <geoscript.geom.bounds.Bounds>` 
    object.

    >>> b = Bounds(0, 0, 1, 1)
    >>> b.scale(1.5)
    (-0.25, -0.25, 1.25, 1.25)
    """
    w = self.width * (factor - 1) / 2
    h = self.height * (factor - 1) / 2

    return Bounds(self.west - w, self.south - h, self.east + w, self.north + h,
       self.proj)

  def expand(self, other):
    """
    Expands this bounds to include another.
    """
    self.expandToInclude(other)
    return self

  def corners(self):
   """
   Returns 4 tuples representing the 4 corners of the Bounds. The ordering is:
   (west,south), (west,north), (east, north), (east, south)
   """
   return [(self.west,self.south), (self.west,self.north), 
      (self.east,self.north), (self.east,self.south)]

  def toPolygon(self):
   """
   Converts the bounding box to a :class:`Polygon <geoscript.geom.polygon.Polygon>`.
   """
   corners = self.corners()
   from geoscript.geom import Polygon
   return Polygon(corners + [corners[0]])

  def tile(self, resx, resy=None):
   """
   Partitions the bounding box into a set of smaller bounding boxes.

   The ``resx`` argument is the horizontal resolution to tile at and should be in the range
   (0,1]. The optional ``resy`` is the vertical resolution and defaults to the same value as
    resx.
   """
   resy = resy if resy is not None else resx
   dx = self.width * resx
   dy = self.height * resy

   y = self.south
   while y < self.north:
     x = self.west
     while x < self.east:
       yield Bounds(x,y,min(x+dx,self.east),min(y+dy,self.north),self.proj)
       x += dx
     y += dy

  def __add__(self, other):
    b = Bounds(env=self)
    if self.proj and other.proj and other.proj != self.proj:
      other = other.reproject(self.proj)
    b.expandToInclude(other)
    return b
    
  def __repr__(self):
    s = '(%s, %s, %s, %s' % (self.west, self.south, self.east, self.north)
    if self.proj:
      s = '%s, %s' % (s, self.proj.id)

    return '%s)' % s

core.registerTypeMapping(ReferencedEnvelope, Bounds, lambda x: Bounds(env=x))

