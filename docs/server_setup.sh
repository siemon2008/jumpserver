#!/bin/bash
# Version: 2.0.0
# Author: LaoGuang
# Date: 2015-04-28

ldap_conf=/etc/openldap/slapd.conf

getSysVersion(){
    cat /etc/redhat-release  | awk '{ print $3 }'
}

echo
echo -e "\033[32m 开始安装Jumpserver v2.0.0 版，期间需要下载软件包，根据网络情况会持续一段时间，并不是卡死. \033[0m"

echo
rpm -q automake &> /dev/null
mini=$?
version=`getSysVersion`
if [ "$mini" != "0" -a "$version" != "6.5" ];then
    echo -n "你确定你的CentOS 6.5 且是最小化安装吗?"
    read confirm
fi
service iptables stop &> /dev/null && setenforce 0
# Install epel and dependency package
#rpm -ivh epel-release-6-8.noarch.rpm &> setup.log && echo "1. 安装epel源 成功" || echo "1. epel已经安装"
yum clean all &> /dev/null 
yum install -y vim automake autoconf gcc xz ncurses-devel patch python-devel git python-pip gcc-c++  &>> setup.log && echo "1. 安装依赖包 成功" || exit 2

# Install mysql
yum -y install mysql mysql-server mysql-devel &> /dev/null
mysql.server start &> /dev/null
mysql -e "drop database if exists jumpserver;create database jumpserver charset='utf8';" || echo "MySQL 密码不对 退出"
mysql -e "grant all on jumpserver.* to 'jumpserver'@'127.0.0.1' identified by 'mysql234';" || exit 2
echo "2. 安装MySQL 成功"

# Clone jumpserver project
tar zxf jumpserver.tar.gz -C /opt
tar xf node_modules.tar.bz2 -C /opt/jumpserver/websocket/
tar xf pip-build-root.tar.bz2 -C /tmp/
cd /opt/jumpserver
#git pull origin master:master && echo "9. 更新代码 成功"
cd /opt/jumpserver/docs
rm -rf /usr/lib64/python2.6/site-packages/Crypto && echo y | pip uninstall pycrypto
#pip install -r requirements.txt -i http://pypi.douban.com/simple &>> setup.log && echo "3. 安装pypi依赖库 成功"
pip install -r requirements.txt &>> setup.log && echo "3. 安装pypi依赖库 成功"

# Config jumpserver conf
cd /opt/jumpserver
read -p "输入本机IP地址：" host
read -p "输入smtp server地址: （如 smtp.qq.com）" smtp_server
read -p "输入smtp server端口: （如 25）" smtp_port
read -p "输入邮件地址: （如 446465001@qq.com) " email
read -p "输入邮箱密码: （如 dfkelfasdf) " password

cf="jumpserver.conf" 
sed -i "s@ip =.*@ip = $host@g" $cf
sed -i "s@web_socket.*@web_socket_host = $host:3000@g" $cf
sed -i "s@email_host = .*@email_host = $smtp_server@g" $cf
sed -i "s@email_port.*@email_port = $smtp_port@g" $cf
sed -i "s/email_host_user.*/email_host_user = $email/g" $cf
sed -i "s/email_host_password.*/email_host_password = $password/g" $cf

echo "4. 修改jumpserver.conf 配置文件 成功"

mkdir -p logs/{connect,exec_cmds} && chmod -R 777 logs
chmod +x *.py *.sh
echo no | python manage.py syncdb
echo

# config websocket
yum -y install nodejs npm &>> setup.log
cd /opt/jumpserver/websocket
npm install &>> setup.log
echo "5. Nodejs 安装并设置完成"
echo "6. 启动服务"
cd /opt/jumpserver
sh service.sh start

cd docs
cp zzjumpserver.sh /etc/profile.d/ 
echo "7. 设置登录运行 成功"
echo "8. 浏览器访问 http://$host/install 初始化 然后登陆，默认账号密码 admin admin 访问http://laoguang.blog.51cto.com/获得帮助"

