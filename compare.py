import sqlite3

db1 = r"/home/ice/Documents/spamLOGS/neo1.db"
db2 = r"/home/ice/Documents/spamLOGS/neo2.db"

conn = sqlite3.connect(db1)
conn.execute("ATTACH ? AS db2", [db2])


# WHERE email IN
# WHERE email NOT IN
res1 = conn.execute(
    """SELECT * FROM Emails
    WHERE email IN
    (SELECT email FROM db2.Emails)
    """).fetchall()

res2 = conn.execute(
    """SELECT * FROM Emails
    WHERE email REGEXP '^n' """).fetchall()
print(res2)
