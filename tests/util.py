from dbexts import dbexts
from nose import SkipTest

def assertClose(test, n, m, tol=1):
  test.assertTrue(abs(n - m) <= tol)

def skipIfNoDB(id):
  try:
    db = dbexts(id, 'dbexts.ini')
  except:
    raise SkipTest()
