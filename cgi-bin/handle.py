#python

import sqlite3,sys

first  = sys.argv[1]
conn = sqlite3.connect("yonghu")
c = conn.cursor()
if (first =="show"):
	kk = "select * from user"	
	ccc = c.execute(kk)
	portlis = sorted([int(str(i[0]).strip("\n")) for i in ccc])
	for j in portlis:
		print j
	quit()
	#print (len(ccc.fetchall()))
	for i in ccc:
		print int(i)

else:
	kk = "delete from user where port = " + first
	ccc = c.execute(kk)
conn.commit()
conn.close()
