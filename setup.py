#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/11'
from setuptools import setup


setup(
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Script',
        'requests',
        'gunicorn',
        'gevent'
    ]
)