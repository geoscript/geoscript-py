from geoscript.util import stats

class Stats_Test:

  def testInterpolate(self):
    vals = stats.interpolate(0,100)
    assert 11 == len(vals)
  
    for i in range(11):
      assert i * 10 == round(vals[i])
