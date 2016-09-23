import sqlite3


db_dir = '/root/workspace/rogue/project/app/rogue.db'


db = sqlite3.connect(db_dir)

result = db.execute("select * from users")
print result.fetchall()
