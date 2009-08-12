import os
import string

ogrepo = 'http://repo.opengeo.org'
m2repo = os.path.join(os.environ['HOME'],'.m2/repository')

def lookup(arg,dirname,names):
   if arg in names:
     url = os.path.join(dirname,arg)[len(m2repo)+1:]

     print 'if [ ! -e target/%s ]; then' % (arg)
     print '\techo "Downloading %s"' % (arg)
     print '\tcurl -G $base/%s -o target/%s' % (url,arg)
     print 'fi'

print 'if [ ! -e target ]; then'
print "\tmkdir target"
print 'fi'

print "base=%s" % ogrepo
for jar in os.listdir('target'):
  os.path.walk(m2repo,lookup,jar)

