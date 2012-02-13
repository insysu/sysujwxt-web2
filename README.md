py-sysu-jwxt
============

python实现的SYSU教务第三方查询网站，作为替代[jwxt.lovemaple.info](http://jwxt.lovemaple.info)的更安全的解决方案。

功能
----

 * 查询分数，支持多学期联合查询，支持未注册，未评教查询
 * 查询课表

部署
----

### 支持平台

 * Linux
 * OS X
 * Windows

### 依赖

 * python2
 * flask
 * pycurl

### 安装

``` bash
sudo apt-get install python python-flask pycurl
git clone git://github.com/humiaozuzu/py-sysu-jwxt.git
cd py-sysu-jwxt
python server.py
```
### 访问

支持浏览器为:

* Firefox
* Chrome
* safari
* IE8+
* opera
* UC（及主流的手机浏览器）

然后访问[http://localhost:5000](http://localhost:5000)即可。如果需要手机访问得到，需要在你的服务器中部署服务。


Todo
----

 * windows平台部署教程
 * 选课功能（因为不评教也可以查询和选课，所以不需要实现这个功能）

