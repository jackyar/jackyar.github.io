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



### 修改软件源

```properties
[base]
name=CentOS-$releasever - Base
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/os/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
 
#released updates
[updates]
name=CentOS-$releasever - Updates
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/updates/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=updates
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
 
#additional packages that may be useful
[extras]
name=CentOS-$releasever - Extras
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/extras/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=extras
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
 
#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-$releasever - Plus
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/centosplus/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=centosplus
gpgcheck=1
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
```



### mysql安装

```shell
# 解压tar
tar -xvf mysql-8.0.30-el7-x86_64.tar.gz
mv mysql-8.0.30-el7-x86_64 /usr/local/mysql
# 创建mysql用户
groupadd mysql
useradd -r -g mysql mysql
# 创建数据存放目录
mkdir -p /data/mysql
chown -R mysql:mysql /data/mysql

vim /etc/my.cnf
------------------------------
[mysqld]
bind-address=0.0.0.0
port=3306
user=mysql
basedir=/usr/local/mysql
datadir=/data/mysql
socket=/tmp/mysql.sock
log-error=/data/mysql/mysql.err
pid-file=/data/mysql/mysql.pid
#character config
character_set_server=utf8mb4
symbolic-links=0
explicit_defaults_for_timestamp=true
------------------------------

./mysqld --defaults-file=/etc/my.cnf --basedir=/usr/local/mysql/ --datadir=/data/mysql/ --user=mysql --initialize
# 查看密码
cat /data/mysql/mysql.err
cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql
# 启动mysql
service mysql start
service mysql status

# 登录mysql修改密码 
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
flush privileges;
use mysql;
update user set host='%' where user = 'root';
flush privileges;

# 连接
ln -s /usr/local/mysql/bin/mysql /usr/bin
```

