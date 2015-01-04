api-doc-manager
===============
API文档管理工具：

普通用户可以浏览API接口，管理员用户可以新增、删除、编辑API接口；

可以实现接口名称、接口描述、接口参数、接口输出、接口调用方式、接口GET/POST实时验证、接口changelog等管理；

工程基于flask，前端基于pure framework

使用方式
===============
- 安装python及相关类库(或运行setup.py)
```python
pip install requests Flask Flask-SQLAlchemy Flask-Script
```

- 修改数据库配置config.py

- 运行manage.py初始化数据库

- 本地直接运行runserver.py

- 服务器部署

请确保已经安装了nginx以及uwsgi
```
cd /usr/local/api_doc(请cd到工程目录)
uwsgi -s /tmp/uwsgi.sock -p 8 -w runserver:app --daemonize /usr/local/nginx/logs/error.log
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

Changelog
===============
1. 新增管理员和普通用户管理，并分别赋予权限，管理员登陆后可以进行增删改查接口，接收用户反馈信息；普通用户登陆后可以关注接口更新，接收接口更新通知，提交接口问题等；
2. 主题变更，好像更大气一点哦；
3. 新增更多便捷操作。

TODO
===============
1. 计划新增测试人员账号和权限管理；
2. 计划新增接口提交管理；
