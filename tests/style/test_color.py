from java import awt
from geoscript.style import Color

class Color_Test:

  def testRGB(self):
    assert Color((255,0,0))._color == awt.Color(255,0,0)
    assert Color('ff0000')._color == awt.Color(255,0,0)
    assert Color('#ff0000')._color == awt.Color(255,0,0)
    assert Color('red')._color == awt.Color(255,0,0)
     
  def testRGBA(self):
    assert Color((255,0,0,128))._color == awt.Color(255,0,0,128)
    assert Color('80ff0000')._color == awt.Color(255,0,0,128)
    assert Color('#80ff0000')._color == awt.Color(255,0,0,128)
    assert Color('red').alpha(128)._color == awt.Color(255,0,0,128)
