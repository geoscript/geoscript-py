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

  def __repr__(self):
    s = '(%s, %s, %s, %s' % (self.l, self.b, self.r, self.t)
    if self.proj:
      s = '%s, %s' % (s, self.proj.id)

    return '%s)' % s

