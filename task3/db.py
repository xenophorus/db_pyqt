import sqlite3
import os


path = os.getcwd()

conn = sqlite3.connect(f'{path}\\..\\test.sql')
cursor = conn.cursor()

cursor.execute("drop table if exists test_table")
conn.commit()

cursor.execute('create table if not exists test_table (id integer primary key, '
               'firstname varchar(255) not null, age integer)')
conn.commit()

cursor.execute("insert into test_table values (1, 'Alex', 25), "
               "(2, 'Betty', 18), (3, 'Helga', 24);")
conn.commit()

cursor.execute("select * from test_table")
res = cursor.fetchall()
print(res)
