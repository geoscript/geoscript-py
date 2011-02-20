import java
import unittest
from geoscript import filter, feature

class Filter_Test:

  def testEvaluate(self):
    fil = filter.Filter('x = 12')
    f1 = feature.Feature({'x': 12})
    f2 = feature.Feature({'x': 13})

    assert fil.evaluate(f1) == True
    assert fil.evaluate(f2) == False


  def testAdd(self):
    fil = filter.Filter('x = 12') + 'y < 10'
    print fil 

    f1 = feature.Feature({'x': 12, 'y': 10})
    f2 = feature.Feature({'x': 12, 'y': 5})

    assert fil.evaluate(f1) == False
    assert fil.evaluate(f2) == True

  def testEquals(self):
    f1 = filter.Filter('x = 12')
    f2 = filter.Filter('x = 12')
    assert f1 == f2
