from org.geotools.geometry import GeneralEnvelope
from org.geotools.geometry.jts import ReferencedEnvelope
from geoscript import proj

class Bounds(ReferencedEnvelope):
  """
  A two dimensional bounding box.
  """
  def __init__(self, l=None, b=None, r=None, t=None, prj=None, env=None):
    if prj:
      prj = proj.Projection(prj)

    if env:
      if isinstance(env, GeneralEnvelope): 
        env = ReferencedEnvelope(env)

      if prj:
        ReferencedEnvelope.__init__(self, env, prj._crs)
      else:
        ReferencedEnvelope.__init__(self, env)
    else:
      ReferencedEnvelope.__init__(self, l, r, b, t, prj._crs if prj else None)

  def getl(self):
    return self.minX()
  l = property(getl)
  """
  The leftmost oordinate of the bounds.
  """

  def getb(self):
    return self.minY()
  b = property(getb)
  """
  The bottomtmost oordinate of the bounds.
  """

  def getr(self):
    return self.maxX()
  r = property(getr)
  """
  The rightmost oordinate of the bounds.
  """

  def gett(self):
    return self.maxY()
  t = property(gett)
  """
  The topmost oordinate of the bounds.
  """

  def getproj(self):
    crs = self.coordinateReferenceSystem
    if crs:
      return proj.Projection(crs)
  proj = property(getproj)
  """
  The :class:`Projection <geoscript.proj.Projection>` of the bounds. ``None`` if the projection is unknown.
  """

  def scale(self, factor):
    """
    Scales the bounds by a particualr factor.

    *factor* is the scale factor. The scale factor must be greather than 0. A 
    value greater than 1 will grow the bounds whereas a value of less than 1 
    will shrink the bounds.
   
    This method returns a new :class:`Bounds <geoscript.geom.bounds.Bounds>` 
    object.

    >>> b = Bounds(0, 0, 1, 1)
    >>> b1 = b.scale(1.5)
    (-0.25, -0.25, 1.25, 1.25)
    """
    w = self.width * (factor - 1) / 2
    h = self.height * (factor - 1) / 2

    return Bounds(self.l - w, self.b - h, self.r + w, self.t + h)
      
  def __repr__(self):
    s = '(%s, %s, %s, %s' % (self.l, self.b, self.r, self.t)
    if self.proj:
      s = '%s, %s' % (s, self.proj.id)

    return '%s)' % s

