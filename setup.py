import os
from distutils.core import setup
from setuptools import find_packages

geotools_libs = ['lib/target/%s' % (f) for f in os.listdir('lib/target')]
setup(name='geoscript',
      version='0.1', 
      description='GeoScript Python',
      author='Justin Deoliveira',
      author_email='jdeolive@opengeo.org',
      url='http://geoscript.org',
      packages=find_packages(),
      data_files=[('geotools', geotools_libs)]
     )
