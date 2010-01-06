from geoscript.feature import Feature
from geoscript.filter import Filter

class Cursor(object):
  """
  A cursor or iterator over :class:`Feature <geoscript.feature.feature.Feature>` objects.
  """

  def __init__(self, reader, layer):
    self.reader = reader
    self.layer = layer

  def next(self):
    """
    Returns the next feature. Raises `StopIteration` if no more features are available.
    """
    if not self.reader.hasNext():
      raise StopIteration

    return Feature(schema=self.layer.schema, f=self.reader.next())
  
  def read(self, n):
    """
    Reads n features into a `list`. If less than n features are available the resulting list will have a size less than n.

    *n* is the number of features to read.
    """
    features = [] 
    for i in range(n):
      try:
        features.append(self.next())
      except StopIteration:
        break

    return features

  def close(self):
    """
    Closes the cursor. This function should *always* be called by client code after the cursor is no longer needed or has been exhausted.
    """
    self.reader.close()

  def __iter__(self):
    return self
