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
DeleteDbFiles.execute('work', 'states', False)
unzip('data/states.db.zip', 'work')
unzip('data/states.shp.zip', 'work')
rmshp('reprojected', 'work')

# init h2 database
db = dbexts('h2', 'dbexts.ini')
db.isql('DROP TABLE IF EXISTS "widgets"')
db.isql('DROP TABLE IF EXISTS "states2"')
db.isql('DROP TABLE IF EXISTS "reprojected"')
db.close()

# init postgresql database
db = dbexts('postgresql', 'dbexts.ini')
def pg_drop(db, tbl):
  try:
    db.isql("DROP TABLE %s" % (tbl))
  except:
    pass
  else:
    db.isql("DELETE FROM geometry_columns WHERE f_table_name='%s'" % (tbl))

pg_drop(db,'widgets')
pg_drop(db,'states2')
pg_drop(db,'reprojected')
db.close()

# init mysql database
db = dbexts('mysql', 'dbexts.ini')
def mysql_drop(db, tbl):
  try:
    db.isql("DROP TABLE %s" % (tbl))
  except:
    pass

mysql_drop(db, 'widgets')
mysql_drop(db, 'states2')
mysql_drop(db, 'reprojected')
db.close()
