
import sqlite3
# setup sqlite
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('drop table if exists Test')
c.execute('create table {tn} (\
          {c1} {t1} primary key,\
          {c2} {t2})'.format(
    tn='Test',
    c1='name',
    t1='text',
    c2='out',
    t2='text',
)
)

# remove all rows from table Emails
c.execute('delete from Test')
# save list of tuples to sqlite table
t0 = ('t1', 'one')
t1 = [('t1', 'one'), ('t2', 'two')]
# insert single tuple to table
c.execute('insert into Test (name, out) values (?,?)', t0)
c.execute('select * from Test')
r0 = c.fetchall()
[print(row) for row in r0]
# delete all rows
c.execute('delete from Test')
# insert list of tuples to table
c.executemany('insert into Test (name, out) values (?,?)', t1)
c.execute('select * from Test')
r1 = c.fetchall()
[print(row) for row in r1]
conn.commit()
conn.close()
