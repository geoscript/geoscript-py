import os
from distutils.core import setup
from setuptools import find_packages

jars = ['jars/%s' % (f) for f in os.listdir('jars')]
setup(name='geoscript',
      version='0.2', 
      description='GeoScript Python',
      author='Justin Deoliveira',
      author_email='jdeolive@opengeo.org',
      url='http://geoscript.org',
      packages=find_packages(),
      data_files=[('jars', jars)],
      scripts=['bin/geoscript-classpath', 'bin/geoscript']
     )
