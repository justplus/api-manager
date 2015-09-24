#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/11'

from apps import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
