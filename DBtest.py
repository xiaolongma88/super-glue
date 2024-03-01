import os
import sqlite3

conn = sqlite3.connect('results.db')
cur = conn.cursor()
# # 执行sql语句
# cur.execute('DELETE FROM Imgs')
# conn.commit()
sql_text_1 = '''SELECT * FROM Imgs'''
cur.execute(sql_text_1)
records = cur.fetchall()
for record in records:
    print(record)

conn.close()