### sshd服务安装

- 使用ssh连接到容器内部

```shell
# 设置密码
passwd

# 升级yum软件包管理器 安装openssh-server
yum -y update
yum -y install vim openssh-server

# 配置sshd配置文件
vim /etc/ssh/sshd_config

PubkeyAuthentication yes #启用公钥私钥配对认证方式 
AuthorizedKeysFile .ssh/authorized_keys #公钥文件路径（和上面生成的文件同） 
PermitRootLogin yes #root能使用ssh登录
ClientAliveInterval 60  #参数数值是秒 , 是指超时时间
ClientAliveCountMax 3 #设置允许超时的次数
# 解决ssh链接缓慢
UseDNS no
GSSAPIAuthentication no
Port 8022 # 设置ssh的连接端口

# 重启ssh服务，并设置开机启动
systemctl restart sshd.service
systemctl enable sshd.service

# 启动容器
docker run -itd -p 8000-9000:8000-9000 -v d:/repos:/opt --privileged --restart=always --name base centos:7 /usr/sbin/init
```



### 多版本GCC配置

```shell
# 安装SCL源
yum -y install centos-release-scl-rh

yum -y install devtoolset-9-gcc devtoolset-9-gcc-c++

# 启用gcc版本
source /opt/rh/devtoolset-9/enable
```



### skynet游戏引擎编译

```shell
git clone https://github.com/cloudwu/skynet.git

# 保证服务器安装gcc make编译工具。 gcc要7或更高版本
yum -y install autoconf
make linux
```



### Samba配置网络共享文件

```shell
# 安装并启动samba服务
yum -y install samba
service smb start [or] systemctl start smb

# 更具需求修改配置
vim /etc/samba/smb.conf
--------------------------------------------
[global]
        workgroup = WORKGROUP
        security = user
        passdb backend = tdbsam
        printing = cups
        printcap name = cups
        load printers = yes
        cups options = raw
        hosts allow = 172.16.6.

[yanyh]
        path = /var/yanyh
        read only = no
        public = yes
        browseable = yes
        writable = yes
        printable = no
        valid users = root,@root
        write list = @root

-------------------------------------------
# 重启samba服务，开放445端口
#####################################
Samba服务所使用的端口和协议： 

1）Port 137 (UDP) - NetBIOS 名字服务 ； nmbd
2）Port 138 (UDP) - NetBIOS 数据报服务
3）Port 139 (TCP) - 文件和打印共享 ； smbd （基于SMB(Server Message Block)协议，主要在局域网中使用，文件共享协议）
4）Port 389 (TCP) - 用于 LDAP (Active Directory Mode)
5）Port 445 (TCP) - NetBIOS服务在windos 2000及以后版本使用此端口, (Common Internet File System，CIFS，它是SMB协议扩展到Internet后，实现Internet文件共享)
6）Port 901 (TCP) - 用于 SWAT，用于网页管理Samba  

# 如果访问不了的话，查看是否关闭selinux
SELinux 有三种工作模式，分别是：

1. enforcing：强制模式。违反 SELinux 规则的行为将被阻止并记录到日志中。

2. permissive：宽容模式。违反 SELinux 规则的行为只会记录到日志中。一般为调试用。

3. disabled：关闭 SELinux。

SELinux 工作模式可以在 /etc/selinux/config 中设定。

# 配置完要reboot重启系统
getenforce                 ##也可以用这个命令检查
```



### Linux 网络设置

```shell
 1、开启防火墙 
     systemctl start firewalld
 ​
 2、开放指定端口
       firewall-cmd --zone=public --add-port=1935/tcp --permanent
  命令含义：
 --zone #作用域
 --add-port=1935/tcp  #添加端口，格式为：端口/通讯协议
 --permanent  #永久生效，没有此参数重启后失效
 ​
 3、重启防火墙
       firewall-cmd --reload
 ​
 4、查看端口号
 netstat -ntlp   //查看当前所有tcp端口·
 ​
 netstat -ntulp |grep 1935   //查看所有1935端口使用情况·
```

