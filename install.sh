#/bin/bash
#author sareeliu

bash sareeliu2.sh install
bash sareeliu2.sh iptable
cp sareeliu2.sh /usr/bin/
/etc/init.d/httpd stop
mv httpd.conf /www/server/apache/conf/
/etc/init.d/httpd start
chmod 777 /usr/local/shadowsocksr/mudb.json