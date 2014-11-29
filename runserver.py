#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/11'
from apps import app

app.run(host='0.0.0.0', debug=False)

#uwsgi
#uwsgi -s /tmp/uwsgi.sock -p 8 -w runserver:app --daemonize /usr/local/nginx/logs/error/log
#nginx
"""
location ~* ^/doc {
	uwsgi_pass unix:/tmp/uwsgi.sock;
    	include uwsgi_params;
	rewrite ^/doc(.*) http://172.16.95.26:5000$1 last;
}
"""