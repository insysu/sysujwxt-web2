py-sysu-jwxt
============

python实现的SYSU教务第三方查询网站，作为替代[jwxt.lovemaple.info](http://jwxt.lovemaple.info)的更安全的解决方案。

功能
----

 * 查询分数，支持多学期联合查询，支持未注册，未评教查询
 * 查询课表(包含时间，支持导出为图片)
 * 查询选课结果
 * 查询学分和绩点

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

### 本地安装使用

Linux和OS X下安装上面的需要的依赖文件即可

Ubuntu下:

``` bash
sudo apt-get install python python-flask pycurl
git clone git://github.com/humiaozuzu/py-sysu-jwxt.git
cd py-sysu-jwxt
python server.py
```

OS X下在终端(搜索bash)中输入:

``` bash
sudo easy_install flask
sudo easy_install pycurl
git clone git://github.com/humiaozuzu/py-sysu-jwxt.git
cd py-sysu-jwxt
python server.py
```

### 作为服务部署

在`templates/base.html`中：

1. 在尾部uncomment掉`route.js`可以实现外网服务器自动跳转到内网服务器以提高访问速度。
2. 开头填入是内网or外网服务器
3. 修改uwsgi.xml并部署(配置uwsgi过程省略)


### 访问

支持浏览器为:

* Firefox
* Chrome
* safari
* IE8+
* opera
* UC（及主流的手机浏览器）

部署好后访问[http://localhost:5000](http://localhost:5000)即可。

updates
-------

Ver 0.4

* css增加对手持设备的支持

Ver 0.3

* 课表添加了时间栏
* 添加查询学分，gpa功能

Ver 0.2

* 添加了查询选课结果的功能
* 添加了选课的接口，但是在web端未实现

Ver 0.1

* 添加了查询分数和课表的功能


Todo
----

 * 选课功能（因为不评教也可以查询和选课，所以不需要实现这个功能）

