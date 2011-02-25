import os
from zipfile import ZipFile
from dbexts import dbexts

# unzip data into work
if not os.path.exists('work'):
  os.mkdir('work')

def unzip(zipfile, todir):
  zip = ZipFile(zipfile)
  for file in zip.namelist():
    target = os.path.join(todir, file)
    if os.path.exists(target):
       continue

    if file.endswith('/'):
       os.mkdir(target)
    else:
       f = open(os.path.join(todir, file), 'w')
       f.write(zip.read(file))
       f.close()

def rmshp(name, dir):
  name = os.path.join(dir, name)
  rm('%s.shp' % name)
  rm('%s.shx' % name)
  rm('%s.dbf' % name)
  rm('%s.prj' % name)
  rm('%s.fix' % name)

def rm(file):
  if os.path.exists(file):
     os.remove(file)

from org.h2.tools import DeleteDbFiles
DeleteDbFiles.execute('work', 'states', True)
unzip('data/states.db.zip', 'work')
unzip('data/states.shp.zip', 'work')
unzip('data/sld_cookbook/point.shp.zip', 'work')
unzip('data/sld_cookbook/line.shp.zip', 'work')
unzip('data/sld_cookbook/polygon.shp.zip', 'work')
rmshp('reprojected', 'work')
rmshp('widgets2', 'work')

# init h2 database
db = dbexts('h2', 'dbexts.ini')
def h2_drop(db, tbl):
  db.isql('DROP TABLE IF EXISTS "%s"' % tbl)
  db.isql('DROP TABLE IF EXISTS "%s_HATBOX"' % tbl)

h2_drop(db, 'widgets')
h2_drop(db, 'widgets2')
h2_drop(db, 'states2')
h2_drop(db, 'reprojected')
db.close()

# init postgresql database
def pg_drop(db, tbl):
  try:
    db.isql("DROP TABLE %s" % (tbl))
  except:
    pass
  else:
    db.isql("DELETE FROM geometry_columns WHERE f_table_name='%s'" % (tbl))

try:
  db = dbexts('postgresql', 'dbexts.ini')
except Exception, e:
  print "Skipping postgis initialization", e
else:
  pg_drop(db,'widgets')
  pg_drop(db,'widgets2')
  pg_drop(db,'states2')
  pg_drop(db,'reprojected')
  db.close()

# init mysql database
def mysql_drop(db, tbl):
  try:
    db.isql("DROP TABLE %s" % (tbl))
  except:
    pass

try:
  db = dbexts('mysql', 'dbexts.ini')
except Exception, e:
  print "Skipping mysql initialization", e
else:
  mysql_drop(db, 'widgets')
  mysql_drop(db, 'widgets2')
  mysql_drop(db, 'states2')
  mysql_drop(db, 'reprojected')
  db.close()
