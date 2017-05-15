# blog-
个人博客系统

本博客系统采用，Django1.9.5 Python2.7 Mysql 5.6 的配置环境来完成的大部分的库都是Django的内置库。

当然也有部分的外界的库比如pymysql

如果你的python环境是python3以及以上的话 需要修改的地方不是很多 

一个是注意一下view.py跟其他py文件下的print问题

另一个 在python2.7版本下models.py采用的是__unicode__方法在3里面改为__str__方法。
