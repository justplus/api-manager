#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/16'
#coding:utf8
from flask import session, url_for, redirect, request
from functools import wraps


def require_login():
    def next(func):
        @wraps(func)
        def decorator(*args, **kw):
            if not session.get('login_name', None):
                return redirect(url_for('site.login'))
            return func(*args, **kw)
        return decorator
    return next

def require_admin():
    def next(func):
        @wraps(func)
        def decorator(*args, **kw):
            if not session.get('login_name', None):
                return redirect(url_for('site.login'))
            elif not session.get('role_name', None) == 'admin':
                return redirect(url_for('site.index'))
            return func(*args, **kw)
        return decorator
    return next