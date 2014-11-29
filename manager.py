#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/11'
from flask.ext.script import Server, Manager, prompt_bool
from apps import app, db

manager = Manager(app)
manager.add_command("runserver", Server('0.0.0.0', port=5000))

@manager.command
def create_all():
    "Creates database tables"
    db.create_all()

@manager.command
def drop_all():
    "Drops all database tables"
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

@manager.command
def hello():
    print 'hello'

if __name__ == "__main__":
    manager.run()