import sqlite3

#1. 연결객체를 만들어라. DBMS회가 driver와 api를 제공한다.
# Server - Client 이게 수요가 많다 FTP(web,hdd)

path='/mnt/c/Users/User/datebase/'
conn=sqlite3.connect(path + '/test3.db')
cur = conn.cursor() #SQL 사용가능한 객체

#sql 실행
sql = '''
CREATE TABLE "person2" (
	"ID"	INTEGER,
	"Name"	TEXT NOT NULL,
	"Pnumber"	TEXT NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
'''

cur.execute(sql)

#sqlite 는 commit
conn.commit #save 단, save 후에 변경불가
