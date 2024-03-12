import os
import sqlite3

def initDB():
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    sql_text_1 = '''
    CREATE TABLE "Imgs" (
        "name" TEXT
     );
     '''
    # 执行sql语句
    cur.execute(sql_text_1)





def findAll():
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("数据库中的表有：", tables)
    # 获取特定表的结构
    cur.execute(f"PRAGMA table_info(Imgs);")
    table_info = cur.fetchall()
    print(f"表z的结构为：", table_info)
    sql_text_1 = '''SELECT * FROM Imgs'''
    cur.execute(sql_text_1)
    records = cur.fetchall()
    for record in records:
        print(record)
    conn.close()

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