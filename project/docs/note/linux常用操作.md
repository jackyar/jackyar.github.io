# linux常用操作

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

```shel
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

### **防火墙及对外开放端口**

```shell
systemctl status[start/stop] firewalld # 查看防火墙状态

# 开启命令
service firewall start

# 查询已开放端口
netstat -ntulp

# 查询端口是否被占用
netstat -anp | grep [port]

firewall-cmd --zone=public --list-port  # 推荐

# 查询指定端口是否开放
firewall-cmd --query-port=6379/tcp

# 添加开放端口，并重新加载 
firewall-cmd --add-port=123/tcp --permanent # 永久开放
firewall-cmd --reload

#移除指定端口
firewall-cmd --permanent --remove-port=123/tcp # 永久移除

```



https://blog.csdn.net/ytangdigl/article/details/79796961 防火墙，网络



### MySQL

```shell
```





update user_auth set password=md5("admin") where id='1';

**开放端口：**



**远赴人间惊鸿宴，一睹人间盛世颜**



```
cd /usr/local/nacos/bin
sh startup.sh -m standalone
```

