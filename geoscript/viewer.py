from geoscript import render
from geoscript.util import deprecated

@deprecated
def draw(g, size=(500,500)):
  """Use :func:`geoscript.render.draw`"""
  render.draw(g, size=size)

@deprecated
def plot(geoms, size=(500,500)):
  """Use :func:`geoscript.render.plot`"""
  render.plot(geoms, size=size)
