import os
import string

ogrepo = 'http://repo.opengeo.org'
m2repo = os.path.join(os.environ['HOME'],'.m2/repository')

def lookup(arg,dirname,names):
   if arg in names:
     url = os.path.join(dirname,arg)[len(m2repo)+1:]

     print '\t\t<get src="%s/%s" dest="jars" usetimestamp="true"/>' % (ogrepo, url)
"""
     print 'if [ ! -e target/%s ]; then' % (arg)
     print '\techo "Downloading %s"' % (arg)
     print '\tcurl -G $base/%s -o target/%s' % (url,arg)
     print 'fi'
"""

"""
print 'if [ ! -e target ]; then'
print "\tmkdir target"
print 'fi'

print "base=%s" % ogrepo
"""
print '<project name="jars" default="jars">'
print '\t<target name="jars">'
for jar in os.listdir('jars'):
  if os.path.splitext(jar)[1] == ".jar":
     os.path.walk(m2repo,lookup,jar)

print '\t</target>'
print '</project>'
