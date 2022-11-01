# KVM 虚拟机安装与管理

参考：https://cloud.tencent.com/developer/article/1703094

```shell
# 安装kvm所需要的软件
yum install -y kvm qemu-kvm qemu-img virt-manager libvirt libvirt-python virt-install virt-client virt-viewer bridge-utils
```

**KVM：它是linux系统内核的一个模块**

**qemu：虚拟化软件**

**qemu-kvm：管理工具（管理网卡等一些设备）**

qemu工具
qemu-kvm：用户空间的工具程序，创建管理虚拟机

qemu-img：是 QEMU 的磁盘管理工具

libvirt工具
GUI：virt-manager, virt-viewer：图形化管理
CLI: virsh, virt-install：创建管理虚拟机

集群工具：
libvirtd：管理虚拟机和其他虚拟化功能，比如存储管理，网络管理的软件集合。Libvirt是一个C工具包的虚拟化功能与最新版本的Linux(以及其他操作系统)。主包包含libvirtd服务器虚拟化支持出口。



### 设置网桥，桥接物理网卡和虚拟网卡

- 修改配置文件

```properties
vi /etc/sysconfig/network-scripts/ifcfg-em1
#文件内容如下：
TYPE=Ethernet
NAME=em1
UUID=b8730dd7-4855-401c-8ad3-5c009969089c    #UUID用自己机器默认的
DEVICE=em1
ONBOOT=yes
BRIDGE=br0   #这个br0是桥接网卡
#文件内容只需要有以上几个就行，其他的都删除或者注释，否则后面会报错
```

- 修改桥接网卡

```properties
vi /etc/sysconfig/network-scripts/ifcfg-br0
#文件内容如下
TYPE=Bridge                 #桥接
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_AUTOCONF=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
IPV6_FAILURE_FATAL=no
BOOTPROTO=static          #静态IP
NAME=br0
DEVICE=br0
ONBOOT=yes
IPADDR=192.168.1.166      #根据自己使用的网络进行设置
NETMASK=255.255.255.0     #根据自己使用的网络进行设置
GATEWAY=192.168.1.1       #根据自己使用的网络进行设置
DNS1=8.8.8.8              #设置一下DNS要不不能上网
DNS2=114.114.114.114
#文件内容只需要有以上几个就行，其他的都删除或者注释，否则后面会报错
```

- 重启网络模块

`systemctl restart network`

`brctl show` 查看网桥

### 虚拟机相关操作

- **创建虚拟机**

```shell
virt-install \
--name=centos7_v1 \
--memory=2048,memory=4096 \
--vcpus=1,maxvcpus=2 \
--os-type=linux \
--os-variant=rhel7 \
--location=/media/CentOS-7-x86_64-Minimal-2009.iso \
--disk path=/kvm/centos7_v1.img,size=30 \
--bridge=br0 \
--graphics=none \
--console=pty,target_type=serial \
--extra-args="console=tty0 console=ttyS0"
```

安装完虚拟机后要设置网络

```shell
ip addr  			# 此时还没有能联网的IP
dhclient eth0  		# 获取IP地址, 这个时候就会有一个新的局域网IP地址
yum -y update  		# 更新yum软件包
yum install -y net-tools  # 安装网络管理工具

cd /etc/sysconfig/network-scripts/
vi ifcfg-eth0 						# 修改ONBOOT的值为yes [ONBOOT=yes]
systemctl restart network  			# 重启网卡服务
```



- **虚拟机配置相关文件**

```shell
ls /etc/libvirt/qemu/

ls /etc/libvirt/qemu/networks/

ls /etc/libvirt/qemu/networks/autostart/
```

- **virsh虚拟机管理常见命令**

```shell
virsh console study01  # 进入指定的虚拟机，进入的时候还需要按一下回车
virsh start study01  # 启动虚拟机
virsh shutdown study01  # 关闭虚拟机
virsh destroy study01  # 强制停止虚拟机
virsh undefine study01  # 彻底销毁虚拟机，会删除虚拟机配置文件，但不会删除虚拟磁盘
virsh autostart study01  # 设置宿主机开机时该虚拟机也开机
virsh autostart --disable study01  # 解除开机启动
virsh suspend study01 # 挂起虚拟机
virsh resume study01 # 恢复挂起的虚拟机
```

