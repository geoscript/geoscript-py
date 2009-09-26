"""
workspace.directory module -- Directory  implementation of Workspace
"""

import os
from java import io, net
from geoscript import util
from geoscript.workspace import Workspace
from org.geotools.data.directory import DirectoryDataStore

class DirectoryWorkspace(Workspace):

  def __init__(self, dir=os.getcwd()):

    ds = DirectoryDataStore(util.toFile(dir), net.URI('http://geoscript.org'))
    Workspace.__init__(self, ds)
