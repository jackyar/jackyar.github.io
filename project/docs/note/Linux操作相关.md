# Linux常用操作汇总

## 通识概念

`文件系统` CentOS 7 默认使用大容量性能较佳的xfs 当默认文件系统

- /dev/sd[ap]1-128：为实体磁盘的磁盘文件名；
- /dev/vd[ad]1-128：为虚拟磁盘的磁盘文件名



## 常用命令

### 基础应用

```shell
date		# 日期时间
cal			# 日历
bc			# 计算器
```

### 磁盘相关

```shell
lsblk		# 列出系统上的所有磁盘列表
fdisk		# 分区，并查看分区信息
smartctl	# 查看硬盘信息
free		# 查看内存
df			# 文件系统挂载点，与使用情况
```

**1、查看磁盘列表** 

(从列表中可以看出，sdb下没有可用分区，可以对其进行分区操作)

![image-20220920122210071](C:\Users\yanyh\AppData\Roaming\Typora\typora-user-images\image-20220920122210071.png)	

**2、磁盘分区操作**

```shell
fdisk /dev/sdb
# -------------------------------
命令(输入 m 获取帮助)：m
命令操作
   a   toggle a bootable flag
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition
   g   create a new empty GPT partition table
   G   create an IRIX (SGI) partition table
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)
# -------------------------------
```

![image-20220920140824214](C:\Users\yanyh\AppData\Roaming\Typora\typora-user-images\image-20220920140824214.png)	

**3、格式化分区，设置文件系统格式，并挂载到机器**

```shell
# 查看磁盘的分区，并对分区进行文件类型格式化
ls /dev/sdb*
# 格式化为ext4类型，也可使用mkfs.xfs格式化为xfs类型
mkfs.ext4 /dev/sdb1
# 挂载都固定文件夹
mkdir /mnt/xf
mount /dev/sdb1 /mnt/xf

# 最后也可以在/etc/fstab中设置开机自动挂载, 然后mount -a

```

![image-20220920144318308](C:\Users\yanyh\AppData\Roaming\Typora\typora-user-images\image-20220920144318308.png)

![image-20220920144651503](C:\Users\yanyh\AppData\Roaming\Typora\typora-user-images\image-20220920144651503.png)	



### 查看系统信息

```shel
uname -a
cat /etc/os-release
```

### 下载源镜像

```shell
/etc/yum.repos.d/CentOS-Base.repo  # 镜像配置文件位置
# 备份系统原来的下载源文件
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
# 获取阿里云的下载源，并写入到文件
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum makecache fast # 刷新缓存
```

### 下载命令

```shell
# -y所有问题全部回答是
yum install -y 软件包  
# 查看工具是包含在哪个软件包下
yum search 软件包
# rz命令安装
yum install -y lrzsz
```

### 网络位置

```shell
/etc/sysconfig/network-script/
```

### vi/vim 编辑

```shell
yy # 拷贝当前行  5yy[从当前行向下拷贝5行]
p # 粘贴拷贝内容
u # 撤销操作
x # 删除单个字符

/查找的内容 # 查找文件中的单词， n 查找下一个
G # 文档末行
gg # 文档首行
:set nu # 显示行号
:20 # 跳到第20行  或者一般模式 20gg
```

- 关机

```shell
shutdown -h now # 立即关机
shutdown -h 1 # 1分钟后关机
shutdown -r now # 重启计算机
halt # 关机
reboot # 立即重启
sync # 将内存数据同步到磁盘，该操作在关机或重启前自动执行

logout # 注销用户
```

### 用户

```shell
useradd 用户名 # 创建用户
useradd -d /home/test 用户名 # 创建用户，并指定用户的家目录
passwd 用户名 # 为用户设置密码

userdel 用户名 # 删除用户
userdel -r 用户名 # 删除用户，同时删除家目录
id 用户名 # 查询用户信息
su - 用户名 # 切换目录 - 表示切换用户，同时切换环境变量， 切换登陆状态
whoami # 查看当前登陆用户 也可以：who am i

groupadd 组名 # 添加用户组
useradd -g 组名 用户名  # 添加用户，并指定到组
usermod -g 组名 用户名  # 需改用户信息

/etc/passwd # 用户配置文件
/etc/shadow # 口令配置文件
/etc/group # 用户组配置文件
```

### **linux系统的运行级别：**

- 0：关机
- 1：单用户 
- 2：多用户没有网络服务
- 3：多用户有网络状态 【常用】
- 4：系统未使用，保留给用户
- 5：图形界面
- 6：系统重启

```shell
init [0-6] # 切换不同的运行级别
# centos7 简化，只使用3,5两个运行级别
multi-user.target # 3
graphical.target # 5

systemctl get-default # 查看当前运行级别
systemctl set-default mutil-user.target # 设置运行级别
```



# Linux 网络设置

https://blog.csdn.net/ytangdigl/article/details/79796961 防火墙，网络

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

- 防火墙对外开放端口

```shell
systemctl status[start/stop] firewalld # 查看防火墙状态
service firewall start # 开启命令

netstat -ntulp # 查询已开放端口
netstat -anp | grep [port] # 查询端口是否被占用
firewall-cmd --zone=public --list-port  # 推荐

# 查询指定端口是否开放
firewall-cmd --query-port=6379/tcp

# 添加开放端口，并重新加载 
firewall-cmd --add-port=123/tcp --permanent # 永久开放
firewall-cmd --reload

#移除指定端口
firewall-cmd --permanent --remove-port=123/tcp # 永久移除
```

- 常用网络命令

```shell
brctl show # 网桥显示
```

https://blog.csdn.net/weixin_46152207/article/details/121007494



# Redis 安装

```shell
# 解压编译
tar -zxvg redis-6.0.16.tar.gz
mv redis-6.0.16.tar.gz /usr/local/redis
cd /usr/local/redis
make
make install

-----------------
daemonize yes         # 后台运行
requirepass catserver # 设置密码

cd /usr/local/bin
redis-server /user/local/redis/redis.conf
```



