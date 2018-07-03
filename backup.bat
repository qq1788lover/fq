#!/usr/bin/bash
# author sareeliu

cp /usr/local/shadowsocksr/mudb.json /www/wwwroot/jiaohuanshengfq.tk/
cp /www/server/apache/conf/httpd.conf /www/wwwroot/jiaohuanshengfq.tk/
cd /www/wwwroot/
zip -r -q .zhujiaohuanshengfq.tk.zip jiaohuanshengfq.tk/ -x "./jiaohuanshengfq.tk/.*"
mv .zhujiaohuanshengfq.tk.zip ./jiaohuanshengfq.tk/
cd /www/wwwroot/jiaohuanshengfq.tk/
rm -rf httpd.conf
cp sareeliu2.sh /usr/bin/
