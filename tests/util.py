def assertClose(test, n, m, tol=1):
  test.assertTrue(abs(n - m) <= tol)
