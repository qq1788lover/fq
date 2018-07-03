#! /usr/bin/env python
# -*- coding: utf-8 -*-

print "Content-type:text/html"
print

import json
import cgi
import time
import os
import sqlite3


# 接受表达提交的数据
form = cgi.FieldStorage()
getuser = form['user'].value.strip()
getpasswd = form['passwd'].value.strip()

'''
getuser = "ceshi1"
getpasswd = "mimaceshi1"
'''

# 加载SSR JSON文件，取出所有的用户名放到列表namelist中
def getname():
    f1 = file("/usr/local/shadowsocksr/mudb.json")
    json1 = json.load(f1)
    f1.close()
    return [i[u'user'] for i in json1]

#，如果用户名可用，则返回用户名相对应的密码
def hgetpasswd(getuser):
    f1 = file("/usr/local/shadowsocksr/mudb.json")
    json1 = json.load(f1)
    f1.close()
    for i in json1:
        if(i[u'user'] == getuser):
            return i[u'passwd']

def chaxun(userport):
    info = "bash sareeliu2.sh userinfo " + str(userport)
    infolist = os.popen(info).readlines()
    # user = infolist[0]     用户名
    global protocol_param
    protocol_param = infolist[1]
    # upflew = infolist[2]
    # downflew = infolist[3]
    global transfer_enable_used
    transfer_enable_used = infolist[4]
    global ss_link
    ss_link = infolist[5]
    global ssr_link
    ssr_link = infolist[6]

def getthetime(getuser, getpasswd):
    conn = sqlite3.connect("yonghu")
    c = conn.cursor()
    res = c.execute("SELECT * FROM user WHERE name=:who AND passwd=:what", {"who": getuser, "what": getpasswd})
    for i in res:
        result = i
    conn.commit()
    conn.close()
    startstamp = result[1]
    global validdays
    validdays = result[3]
    endstamp = startstamp + validdays * 24 * 60 * 60
    currentstamp = int(time.time())
    timebetween1 = int(round((endstamp - currentstamp) / (3600 * 24)))
    timebetween2 = timebetween1 + 1
    global timebetween
    if (timebetween2 == 0):
        timebetween = "24:00到期！"
    else:
        timebetween = timebetween1

# res = c.execute("select * from user where name==? and passwd == ?",(getuser,getpasswd))
# 从数据库中查询出所有的用户名和密码

conn = sqlite3.connect("yonghu")
c = conn.cursor()
passwdres = c.execute("SELECT * FROM user WHERE name==?", (getuser,))
k=[]
for i in passwdres:
        k.append(i)
conn.commit()
conn.close()


#0代表没有用户名对应的密码，即数据表中不存在该用户名，即为不存在的用户名，需要提示用户名或者密码错误
if(len(k)==0):
    tips = "用户名或密码输误，请重试！"
    protocol_param = ""
    validdays = ""
    transfer_enable_used = ""
    ss_link = ""
    timebetween = ""
    yanzheng = "no"

#用户名在数据库里面有记录，则要继续判断是否在后台文件中是否有数据
else:
    k=k[0]
    dataname = k[4]
    yanzheng = "ok"
    dataport = k[0]
    namelist = getname()
    #用户名在后台中也有记录
    if(dataname in namelist):
        chaxun(dataport)
        #从后台取出该用户名对应的密码，如果和提交的密码相同则提示登录成功，否则用户名密码错误
        passwdlist = hgetpasswd(getuser)
        if (getpasswd == passwdlist):
            getthetime(getuser, getpasswd)
            tips = "欢迎回来，登录成功"
        else:
            tips = "用户名或密码输误，请重试！"
            protocol_param = ""
            validdays = ""
            transfer_enable_used = ""
            ss_link = ""
            timebetween = ""
            yanzheng = "no"
    else:
		#如果用户名在后台中没有记录，就是账号过期了
        tips = "账号已到期，停止使用！"
        protocol_param = ""
        validdays = ""
        transfer_enable_used = ""
        ss_link = ""
        timebetween = ""    

header = '''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta content="IE=edge" http-equiv="X-UA-Compatible">
	<meta content="initial-scale=1.0, width=device-width" name="viewport">
	<title>jiaohuanshengFQ.tk</title>
	<link href="../css/base.min.css" rel="stylesheet">
	<script type='text/javascript' src='https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js'></script>
  	<script src="../js/base.min.js" type="text/javascript"></script>
	<script type='text/javascript' src='https://static.runoob.com/assets/qrcode/qrcode.min.js'></script>
</head>
<body>
    <div class="content">
        <div class="content-heading">
            <div class="container">
                <h1 class="heading" >账号与配置教程</h1>
            </div>
        </div>
        <div class="content-inner">
            <div class="container">
	<body>
		<div class="card-wrap">
			<div class="row">
'''
section1 = '''
				<div class="col-lg-3 col-sm-6">
					<div class="card card-green">
						<div class="card-main">
                          <div class="card-inner">
                             	<p><strong>账号信息</strong></p>
								<p><strong>提示：</strong><span style="color:red" id="myjiance"> %s </span></p>
								<p><strong>您的用户名：</strong><span id="myname"> %s</span> </p>
								<p><strong>您的密码：</strong> <span id ="mypasswd">%s </span></p>
								<p><strong>设备限制数：</strong> %s </p>
                            	<p><strong>账号总天数：</strong><span style="color:red"> %s </span></p>
                            	<p><strong>剩余的天数：</strong><span style="color:red"> %s </span></p>
                           		<p>账号会于最后一天的24:00过期！</p>
								<p><strong>已使用的总流量：</strong> %s</p>
								<button class="form-group-btn btn" onclick=post()>另一个节点可供选择</button>
                                <button id="sslinkbtn" class="form-group-btn btn">获取安卓用的链接(需复制)</button>
								<div style="word-break: break-all;word-wrap: break-word;display:none" id='sslink'><sapn style="color:blue">%s</span></div>
                            	<button id='ssbutton' class="form-group-btn btn">获取苹果,winds系统用的二维码</button>
								<div  style="display:none" id='showssqrcode' class="card-img"></div>
								<p style="color:red">安卓请复制完整的蓝色链接。苹果和windows系统请扫描二维码，在安装的软件里扫。具体请按照教程来！</p>
							    <a href="#appleAnchor">查看苹果手机教程</a>
                                <a href="#windowsAnchor">查看windows教程</a>
                            	<p></p>
                          </div>

							<div class="card-action">
								<ul class="nav nav-list pull-left">
									<li>
										<a href="../index.html"><span class="icon icon-check"></span>返回主页面</a>
									</li>
								</ul>
							</div>

                      	</div>
					</div>
				</div>
'''
              
section2 = '''

				<div class="col-lg-3 col-sm-6">
					<div class="card card-green">
						<div class="card-main">
							<div class="card-inner">
								<p><strong>安卓手机配置</strong></p>
								<p><strong>一：</strong> 下载安装软件<a href="../software/base.apk">点我下载</a></p>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>二：</strong>方法1:打开软件，点击右上角"+"按钮，会看见扫描二维码选项，扫描账号信息中二维码。<text style="color:red">或者方法2：针对安卓手机，从账号信息中复制链接，在软件“+”处选择从剪贴板导入，会自动配置完成 </p>
                              	<img src="../img/android/android01.png" class="card-img" style="width:250px;height:500px"/>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>三：</strong> 二维码扫描或剪贴板导入完成后，会生成一条配置。选中该配置（选中会变色）</p>
                             	<img src="../img/android/android02.png" class="card-img" style="width:250px;height:500px"/>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>四：</strong> 选中后，点击右下角带斜杠的纸飞机图标，其上斜杠会消失。同时手机屏幕最上方会出现小钥匙图标。代表软件启动成功。</p>
                              	<img src="../img/android/android03.png" class="card-img" style="width:250px;height:500px"/>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>五：</strong> 按上述步骤，其他按钮选项不用理会，应该可以翻出去了。 </p>
                              	<img src="../img/android/android04.png" class="card-img" style="width:250px;height:500px"/>
                                <p style="word-break: break-all;word-wrap: break-word;"><strong>六：</strong> 不再用的时候，进入软件。点击纸飞机按钮会有斜杠出现就是关闭。 </p>
                          	</div>
						</div>
					</div>
				</div>

'''
              
section3 = '''
              <div class="col-lg-3 col-sm-6">
					<div class="card card-green">
						<div class="card-main">
							<div class="card-inner">
								<p id = "appleAnchor"><strong>苹果手机配置</strong></p>
                                <p style="word-break: break-all;word-wrap: break-word;"><strong>一：</strong>在苹果应用商店搜索ssrconnectpro下载安装。<a href="https://itunes.apple.com/cn/app/ssrconnectpro/id1272045249?mt=8">点我跳转下载</a></p>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>二：</strong>进入软件，点击左上角扫描二维码按钮，扫描账号信息中的二维码</p>
                              	<img src="../img/apple/apple01.jpg" class="card-img" style="width:250px;height:500px"/>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>三：</strong>扫描完成后，会提示起个名字，默认dafault就行。然后有一条配置信息。 </p>
                              	<img src="../img/apple/apple02.jpg" class="card-img" style="width:250px;height:500px"/>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>四：</strong>选中该配置信息，其前的纸飞机图标会变色。然后跳转回主页面</p>
                              	<img src="../img/apple/apple03.jpg" class="card-img" style="width:250px;height:500px"/>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>五：</strong>在主界面中点击 connect 按钮启动，屏幕最上方会有vpn图标显示。不再用的时候，点击 stop 就是关闭。</p>
                              	<img src="../img/apple/apple04.jpg" class="card-img" style="width:250px;height:500px"/>
							</div>
						</div>
					</div>
				</div>
'''
              
section4 = '''
              <div class="col-lg-3 col-sm-6">
					<div class="card card-green">
						<div class="card-main">
							<div class="card-inner">
								<p id = "windowsAnchor"><strong>windows系统配置</strong></p>
                              	<p style="word-break: break-all;word-wrap: break-word;"><strong>一：</strong>下载软件<a href="../software/Shadowsocks.exe">点我下载</a> </p>
                              	<img src="../img/wins/wins01.png" class="card-img" style="width:100px;height:100px"/>
                              	<p style="word-break: break-all;word-wrap: break-word;"><strong>二：</strong>下载的是个纸飞机图标的exe可执行文件，双击启动，此时电脑屏幕右下角会有小纸飞机图标（可能会折叠隐藏），鼠标右键单击它，选中“服务器” 选项。</p>
                              	<img src="../img/wins/wins03.png" class="card-img" style="width:250px;height:200px"/>
                                <p style="word-break: break-all;word-wrap: break-word;"><strong>三：</strong>如果弹框提示：.NET Framwork版本过低，请点 确定 升级.NET运行环境。升级之后，就能正常启动</p>
                              	<img src="../img/wins/wins02.png" class="card-img" style="width:250px;height:200px"/>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>四：</strong>在“服务器”选项下，选择“扫描桌面上方的二维码”，软件会自动识别出二维码并配置完成。（<span style="color:red">注意：屏幕中需要能看见账号信息中的二维码，才会自动扫描完成</span>）</p>
                              	<img src="../img/wins/wins04.jpg" class="card-img" style="width:250px;height:200px"/>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>五：</strong>扫描完成，在新对话框中，一定要<span style="color:red">先选中生成的配置，再点确定按钮。</span></p>
                              	<img src="../img/wins/wins05.jpg" class="card-img" style="width:250px;height:200px"/>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>六（重要）：</strong>按步骤四图片，回到菜单中，<span style="color:red">①选中启动系统代理，②代理模式选择为全局模式，③允许来自局域网的连接。（这三步别忘了！）</span></p>
								<p style="word-break: break-all;word-wrap: break-word;"><strong>七：</strong>按上述步骤配置后，应该就能翻出去。不再用时，鼠标右键单击屏幕右下角纸飞机退出软件即可</p>
							</div>
						</div>
					</div>
				</div>
'''
              
section5 = '''
              <div class="col-lg-3 col-sm-6">
					<div class="card card-green">
						<div class="card-main">
							<div class="card-inner">
								<p id = "windowsAnchor"><strong>合作伙伴</strong></p>
                              	<img src="../img/xieyuzhe02.jpg" class="card-img" style="width:250px;height:200px"/>
                                <img src="../img/xieyuzhe01.jpg" class="card-img" style="width:250px;height:200px"/>
							</div>
						</div>
					</div>
				</div>
'''
              
footer = '''


			</div>
		</div>

          </div>
        </div>
    </div>
	<footer class="footer">

      <div class="container">
			<p>JiaohuanshengFq.tk</p>
		</div>
	</footer>



<script type='text/javascript'>
  //$("#ssbutton").one("click",a);
 // function a(){
			var myssqrcode = new QRCode(document.getElementById('showssqrcode'), {
			render   : "table",
  			width : 200,
			height : 200
 	})
		var ssText = document.getElementById('sslink').innerText;
			if (ssText != "")
    		myssqrcode.makeCode(ssText);
   // }
  //document.getElementById('showssqrcode')
  $("#ssbutton").click(function(){
     $("#showssqrcode").toggle();
  })
</script>

<script type='text/javascript'>
  		$("#sslinkbtn").click(function(){
          $("#sslink").toggle();
 })
</script>

<script type='text/javascript'>
	$("#ssrbutton").one("click",function(){
			var myssrqrcode = new QRCode(document.getElementById('showssrqrcode'), {
				render   : "table",
  				width : 200,
				height : 200
	})
	var ssrText = document.getElementById('ssrqrcode').innerText;
  		//alert(ssrText)
  		if (ssrText != "")
			myssrqrcode.makeCode(ssrText);})
</script>

<script>
  
function post() {
  var username =  document.getElementById('myname').innerText
  var password =  document.getElementById('mypasswd').innerText
  
  var myform = document.createElement("form");
    myform.action = "http://us.jiaohuanshengfq.tk/cgi-bin/show_info.py" + "?token="+Math.floor(Math.random()*10+1);
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
      
<p></p>
</body>
</html>
'''
print header
print section1 % (tips, getuser, getpasswd, protocol_param, validdays, timebetween, transfer_enable_used, ss_link)
if (yanzheng == "ok"):
    print section2
    print section3
    print section4
    print section5
print footer