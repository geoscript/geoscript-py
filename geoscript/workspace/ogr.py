import os
from java.util import HashMap
from geoscript.workspace import Workspace
from org.geotools.data.ogr.jni import JniOGRDataStoreFactory

class OGR(Workspace):
  def __init__(self, dataset, driver=None):

    params = {'DatasourceName': dataset}
    if driver:
      params['DriverName'] = driver
    Workspace.__init__(self, JniOGRDataStoreFactory(), HashMap(params))
