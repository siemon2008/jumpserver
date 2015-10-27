#欢迎使用Jumpserver
**Jumpserver**是一款由python编写开源的跳板机(堡垒机)系统，实现了跳板机应有的功能



> **统计管理** 统一管理用户 
> 
> **授权** 授权用户登录特定主机
> 
> **审计** 审计用户操作
> 
> **web管理** 漂亮的web管理界面

## 主要模块
#### 用户管理 ####
	负责用户管理，添加用户，编辑用户，建立部门，建立用户组等
#### 资产管理 ####
	负责资产管理，添加资产，编辑资产，建立IDC，建立用户组等
#### 授权管理 ####
	负责授权用户登录某些特定主机，授权sudo，查看授权申请
#### 日志审计 ####
	负责用户操作的审计，监控用户操作，统计用户操作记录，中断用户操作
#### 上传下载 ####
	负责用户文件上传下载
#### Sshd配置 ####
	通过/etc/ssh/sshd_config配置限制用户登录堡垒机服务器上,只允许用户执行connect.py脚本.	
        rm /etc/profile.d/zzjumserver.sh
        vim /etc/ssh/sshd_config 
        Match User "!root,*"
          ForceCommand /usr/bin/python  /opt/jumpserver/connect.py
          AllowAgentForwarding yes
          AllowTcpForwarding  yes
          X11Forwarding yes
#### VIM高显配置 ####
	vim /etc/profile
	export TERM=xterm-color

[官网](http://www.jumpserver.org)

[demo站点](http://demo.jumpserver.org)

[更新log](http://laoguang.blog.51cto.com/6013350/1635853)

[部署文档](http://laoguang.blog.51cto.com/6013350/1636273)


