#! /usr/bin/env python
# -*- coding: utf-8 -*-

#print "Content-type:text/html"
#print

import json
import cgi
import urllib2
import os

# 获取提交的数据
form = cgi.FieldStorage() 
getcode = form['code'].value

f = open("table","w")
f.seek(0,0)
f.write(getcode)
f.seek(0,0)
f.close()


print('Content-type:text/html\n\n')
print('<html>')
print ('<head>')
print ('<meta charset="utf-8">')
print('<title>交换生FQ</title>')
print ('</head>')
print ('<body>')
print ('<h2>添加成功！</h2>')
print ('</body>')
print ('</html>')




