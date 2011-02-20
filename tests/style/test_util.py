import java
import unittest
from geoscript.style import util

class Style_Test:

  def testColorFromName(self):
    col = util.color('red')
    assert 255 == col.red
    assert 0 == col.green
    assert 0 == col.blue
    
  def testColorFromTuple(self):
    col = util.color((12,34,56))
    assert 12 == col.red
    assert 34 == col.green
    assert 56 == col.blue
    
  def testColorFromHex(self):
    col = util.color("0a0bff")
    assert 10 == col.red
    assert 11 == col.green
    assert 255 == col.blue

    col = util.color("#0a0bff")
    assert 10 == col.red
    assert 11 == col.green
    assert 255 == col.blue
