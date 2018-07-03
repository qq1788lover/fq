#! /usr/bin/env python
# -*- coding: utf-8 -*-

print "Content-type:text/html"
print

import json
import cgi
import os
import time
import sqlite3
import socket,sys, traceback 

# 从前端获取提交的数据
form = cgi.FieldStorage()
getuser = form['user'].value
getpasswd = form['passwd'].value
signcode = form['signcode'].value

# 加载SSR JSON文件，取出所有的用户名放到列表namelist中
def getname():
    f1 = file("/usr/local/shadowsocksr/mudb.json");
    json1 = json.load(f1);
    f1.close();
    return [i[u'user'] for i in json1];
#  加载SSR JSON文件，取出所有的端口号放入 portlist 中，并计算出为新注册用户分配端口号

def getport():
    f1 = file("/usr/local/shadowsocksr/mudb.json");
    json1 = json.load(f1);
    f1.close();
    portlist = [i[u'port'] for i in json1];
    for i in range(2333,2600):
        if i not in portlist:
            return i
            break

#从注册码表中取出注册码，放入codelist中
def getcode():
    f2 = open("table", "r")
    lines = f2.readlines()
    codelist0 = []
    for line in lines:
        temp = line.strip('\n')
        codelist0.append(temp)
    f2.close()
    return codelist0
	

namelist = getname()
codelist = getcode()

# 如果用户名是新的，且注册码可用
if (getuser not in namelist and signcode in codelist):
    # 从用户提交的注册码中分析出使用天数，赋值给validdays
    validdays = int(signcode[5:])
    # 注册码在codelist中，则在codelist中删除该注册码，并把剩下的注册码下回到文件中
    f3 = open("table", "w")
    codelist.remove(signcode)
    #		new = list(everycode.strip("\n") for everycode in codelist)
    for everycode in codelist:
        f3.write(everycode)
        f3.write("\n")
    # f3.write(map(lambda x:x+"\n",info22))
    f3.close()
    # 注册码处理完毕，现在进行注册账号操作
    #给用户分配端口号码
    newport = int(getport())
    register = "sareeliu2.sh adduser {0} {1} {2}".format(getuser, getpasswd,newport)
    registerinfo = os.popen(register).readlines()
    #userport = registerinfo[0]
    info = "sareeliu2.sh userinfo " + str(newport)
    infolist = os.popen(info).readlines()
    info2 = "处理注册码成功！"
    info1 = "注册成功"
    info3 = "准备跳转,倒计时:"
    ss_link = infolist[5]
    ssr_link = infolist[6]
    # 账号生成完毕，进行插入数据表操作
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    timestamp = int(time.time())
    conn = sqlite3.connect("yonghu")
    c = conn.cursor()
    c.execute("INSERT INTO user VALUES(?,?,?,?,?,?)",(newport, timestamp, time1, int(validdays), getuser, getpasswd))
    conn.commit()
    conn.close()
    #以下是socket代码，
    host = '107.172.207.23'  
    port = 7878    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    try:  
        s.connect((host, port))  
    except Exception as e:  
        msg = traceback.format_exc()  
        print ("wrong", msg)    
    input_command = "sareeliu2.sh adduser {0} {1} {2}".format(getuser,getpasswd,newport)
    s.send((input_command).encode())  
    s.shutdown(1)  
    while 1:   
        buff = s.recv(4096)  
        if not len(buff):  
            break  
        #sys.stdout.write(str(buff))

# 如果用户名是新的，但注册码没在codelist中
elif (getuser not in namelist and signcode not in codelist):
    info1 = "用户名可用"
    info2 = "注册码不可用！！"
    info3 = "注册失败！"
    getuser = ""
    getpasswd = ""
    ss_link = ""
    ssr_link = ""
# 如果用户名都被占用了
else:
    info1 = "用户名被占用，请更换！！"
    info2 = "因用户名被占用，不会检测注册码"
    info3 = "注册失败！！"
    getuser = ""
    getpasswd = ""
    ss_link = ""
    ssr_link = ""

header = '''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta content="IE=edge" http-equiv="X-UA-Compatible">
	<meta content="initial-scale=1.0, width=device-width" name="viewport">
	<title>用户注册</title>
	<link href="../css/base.min.css" rel="stylesheet">
	<script type='text/javascript' src='https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js'></script>
	<script type='text/javascript' src='https://static.runoob.com/assets/qrcode/qrcode.min.js'></script>
</head>
<body>
    <div class="content">
        <div class="content-heading">
            <div class="container">
                <h1 class="heading">新用户注册</h1>
            </div>
        </div>
        <div class="content-inner">
            <div class="container">
'''
footer = '''
</div>
        </div>
    </div>
	<footer class="footer">

      <div class="container">
			<p>JiaohuanshengFQ.tk</p>
		</div>
	</footer>
<script type='text/javascript'>
  $("#ssbutton").one("click",function(){
		var myssqrcode = new QRCode(document.getElementById('showssqrcode'), {
		render   : "table",
  		width : 200,
		height : 200
 })
var ssText = document.getElementById('ssqrcode').innerText;
//alert(ssText);
 if (ssText != "")
    myssqrcode.makeCode(ssText); });
</script>

<script type='text/javascript'>
$("#ssrbutton").one("click",function(){
		var myssrqrcode = new QRCode(document.getElementById('showssrqrcode'), {
			render   : "table",
  			width : 200,
			height : 200
		})
var ssrText = document.getElementById('ssrqrcode').innerText;
 // alert(ssrText)
  	if (ssText != "")
		myssrqrcode.makeCode(ssrText);})
</script>
	<script src="../js/base.min.js" type="text/javascript"></script>

<script type="text/javascript">

  var jiance =  document.getElementById('myjiance').innerText
  var myname =  document.getElementById('myname').innerText
  var mypasswd =  document.getElementById('mypasswd').innerText
  if (jiance == "注册成功"){
 	setTimeout("post(myname,mypasswd)",3000)
  	setInterval("showint()",1000)
  }
  var i = 5;
function showint(){
	if(i > 0){document.getElementById('showint').innerText = i
  	i --;
}
  else{console.log(i)
	}}

function post(username,password) {
    var myform = document.createElement("form");
    myform.action = "https://jiaohuanshengfq.tk/cgi-bin/show_info.py" + "?token="+Math.floor(Math.random()*10+1);
    myform.method = "post";
    myform.style.display = "none";

    var userinput = document.createElement("input");
    userinput.type = "text";
    userinput.name = "user";
    userinput.value = username;
    myform.appendChild(userinput);

    var passwdinput = document.createElement("input");
    passwdinput.type = "text";
    passwdinput.name = "passwd";
    passwdinput.value = password;
    myform.appendChild(passwdinput);

    document.body.appendChild(myform);
    myform.submit();
    return myform;
}
</script>


</body>
</html>
'''
formhtml = '''

<!--<div class="card-wrap">
					<div class="column">-->
						<div class="col-lg-12 col-sm-12">
							<div class="card card-green">
								<!--<a class="card-side" href="/"><span class="card-heading">账号使用信息</span></a>-->
								<div class="card-main">
									<div class="card-inner">
                                      	<p><strong>检测用户名：</strong> <span style="color:red;font-size:22px" id="myjiance">%s</span> </p>
                                      	<p><strong>处理注册码：</strong>%s</p>
                                      	<p><strong>用户名为：</strong><span id="myname">%s</span> </p>
										<p><strong>密码：</strong><span id="mypasswd">%s</span></p>
										<!--<p style="color:red ;word-break: break-all;word-wrap: break-word;">链接和二维码中均含有FQ配置信息。选择一种方式导入到软件中即可使用</p>
                                      	<strong >链接:</strong><p id='ssqrcode'>%s</p>
                                      	<button id='ssbutton' class="btn">获取二维码</button>
      						            <div id='showssqrcode' style="word-break: break-all;word-wrap: break-word;"></div>
                                      	<p style="color:red;word-break: break-all;word-wrap: break-word;">如果提示新用户注册成功，则可去<a href="../login.html">登录界面</a>查看手机电脑配置教程！</p>
										<strong>SSR链接：</strong><div id='ssrqrcode'>%s</div>
                              			<button id='ssrbutton'>获取SSR二维码</button>
                              			<div id='showssrqrcode' style="word-break: break-all;word-wrap: break-word;"></div>-->
                                      <p><span style="color:red;font-size:20px">%s</span><span id="showint" style="color:red;font-size:22px"></span></p>

									</div>
									<div class="card-action">
										<ul class="nav nav-list pull-left">
											<li>
												<a href="../login.html"><span class="icon icon-check"></span>未跳转，点我手动登录</a>
											</li>
										</ul>
									</div>
								</div>
							</div>
					</div>
			 <!--</div>
</div>-->
'''

# 打印返回的内容
print header
print formhtml % (info1, info2, getuser, getpasswd, ss_link, ssr_link, info3)
print footer
