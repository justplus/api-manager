api-doc-manager
===============
API文档管理工具：

普通用户可以浏览API接口，管理员用户可以新增、删除、编辑API接口；

可以实现接口名称、接口描述、接口参数、接口输出、接口调用方式、接口GET/POST实时验证、接口changelog等管理；

工程基于flask，前端基于pure framework

使用方式
===============
- 安装python及相关类库
```python
pip install requests, Flask, Flask-SQLAlchemy, Flask-Script
```

- 修改数据库配置

见config.py

- 运行manage.py初始化数据库

- 本地直接运行runserver.py

- 服务器部署

请确保已经安装了nginx以及uwsgi
```
cd /usr/local/api_doc(请cd到工程目录)
uwsgi -s /tmp/uwsgi.sock -p 8 -w runserver:app --daemonize /usr/local/nginx/logs/error/log
```

nginx可做如下设置：
```
location ~* ^/doc {
	uwsgi_pass unix:/tmp/uwsgi.sock;
    	include uwsgi_params;
	rewrite ^/doc(.*) http://xxx.xx.xx.xx:5000$1 last;
}
```

这样你就可以通过`http://domain or xxxx.xx.xx.xx/doc`访问了

TODO
===============
1. 新增管理员账户管理
2. 普通用户登录后关注接口changelog并提醒
