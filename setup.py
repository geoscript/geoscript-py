import os
import shutil
from distutils.core import setup, Command
from distutils.archive_util import make_tarball
from setuptools import find_packages

class SrcCmd(Command):
    description = "custom command to build archive of only py sources"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        base_dir = self.distribution.get_fullname()
        base_name = os.path.join('dist', base_dir)

        for fmt in ['zip', 'gztar']:
          file = self.make_archive(base_name+'-src',fmt,base_dir='geoscript')
          self.distribution.dist_files.append(file)

class DocCmd(Command):
    description = "custom command to build archive for docs"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        base_dir = self.distribution.get_fullname()
        base_name = os.path.join('dist', base_dir)

        doc_base = 'doc/.build/html'
        for fmt in ['zip', 'gztar']:
          file = self.make_archive(base_name+'-doc',fmt,doc_base)
          self.distribution.dist_files.append(file)


ver='1.3-20130322'
jars = ['jars/%s' % (f) for f in os.listdir('jars')]
setup(cmdclass={'src': SrcCmd, 'doc': DocCmd}, 
      name='geoscript',
      version=ver,
      description='GeoScript Python',
      author='Justin Deoliveira',
      author_email='jdeolive@opengeo.org',
      url='http://geoscript.org',
      packages=find_packages(),
      data_files=[('jars', jars)],
      scripts=['bin/geoscript-classpath', 'bin/geoscript', 'bin/geoscript.bat']
     )

