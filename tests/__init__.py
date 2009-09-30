import os
from zipfile import ZipFile
from dbexts import dbexts

# unzip data into work
if not os.path.exists('work'):
  os.mkdir('work')

zip = ZipFile('data/states.db.zip')
for file in zip.namelist():
  target = os.path.join('work',file)
  if os.path.exists(target):
     continue

  if file.endswith('/'):
     os.mkdir(target)
  else:
     f = open(os.path.join('work',file), 'w')
     f.write(zip.read(file))
     f.close()

# init h2 database
db = dbexts('h2', 'dbexts.ini')
db.isql('DROP TABLE IF EXISTS "widgets"')
db.isql('DROP TABLE IF EXISTS "states2"')
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
db.close()
