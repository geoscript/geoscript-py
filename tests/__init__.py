from dbexts import dbexts

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
