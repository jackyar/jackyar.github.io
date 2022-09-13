## 命令汇总

### 通识概念

`文件系统` CentOS 7 默认使用大容量性能较佳的xfs 当默认文件系统

- /dev/sd[ap]1-128：为实体磁盘的磁盘文件名；
- /dev/vd[ad]1-128：为虚拟磁盘的磁盘文件名



### 基础指令

```shell
date		# 日期时间
cal			# 日历
bc			# 计算器
-------------------------
lsblk		# 列出系统上的所有磁盘列表
fdisk		# 分区，并查看分区信息
smartctl	# 查看硬盘信息
free		# 查看内存
df			# 文件系统挂载点，与使用情况
```



## Linux 网络设置

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



## Redis 安装

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



## KVM 虚拟机安装与管理

yum install qemu-kvm qemu-kvm-tools virt-manager libvirt -y



**KVM：它是linux系统内核的一个模块**

**qemu：虚拟化软件**

**qemu-kvm：管理工具（管理网卡等一些设备）**

