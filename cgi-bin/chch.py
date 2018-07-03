#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3,time,os
import socket,sys,traceback 


def mysocket(port): 
    host = '107.172.207.23'  
    port = 7878  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    try:  
        s.connect((host, port))  
    except Exception as e:  
        msg = traceback.format_exc()  
        print ("wrong", msg)  
    input_command = "sareeliu2.sh deluser {0}".format(port)
    s.send((input_command).encode())  
    s.shutdown(1)  
    while 1:   
        buff = s.recv(4096)  
        if not len(buff):  
            break  
        #sys.stdout.write(str(buff))	

conn = sqlite3.connect("yonghu")
c = conn.cursor()
res = c.execute("select * from user")
reslis = [ i for i in res]
for i in reslis:
	endtime = int(i[1]) + i[3]*24*3600
	currenttime = int(time.time())
	if (endtime < currenttime):
		#c.execute("delete from user where port==?",(i[0],))
		command = "sareeliu2.sh deluser "+ str(i[0])
		os.system(command)
		mysocket(i[0])                               
		print ("delete" + str(i[4]))
	else:
		#print "不删除"
		pass
conn.commit()
conn.close()
                               
                  
