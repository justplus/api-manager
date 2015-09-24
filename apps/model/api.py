#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/11'
from apps import db
from datetime import datetime


class Api(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    api_description = db.Column(db.String(255), nullable=False, index=True)
    api_format = db.Column(db.String(50), nullable=False)
    api_method = db.Column(db.String(50), nullable=False)
    api_auth = db.Column(db.Boolean)
    api_notice = db.Column(db.Text)
    api_return = db.Column(db.Text)
    api_category = db.Column(db.Integer, db.ForeignKey('category.id'))
    api_test = db.Column(db.String(500))
    api_view_count = db.Column(db.Integer, default=0)
    api_collect_count = db.Column(db.Integer, default=0)
    api_params = db.relationship('Param', cascade="all, delete-orphan",
                    passive_deletes=True)
    api_changelog = db.relationship('Changelog', cascade="all, delete-orphan",
                    passive_deletes=True)

    def __repr__(self):
        return '<API %r>' % self.api_name


class Param(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    param_name = db.Column(db.String(50), nullable=False)
    param_description = db.Column(db.String(255), nullable=False)
    param_must = db.Column(db.Boolean, nullable=False)
    param_type = db.Column(db.String(50), nullable=False)
    param_default = db.Column(db.String(50))
    api_id = db.Column(db.Integer, db.ForeignKey('api.id', ondelete='CASCADE'))
    #api = db.relationship('Api', backref='params', lazy='dynamic')

    def __repr__(self):
        return '<Param %r>' % self.param_name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20), unique=True, nullable=False)
    api = db.relationship('Api', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.category_name


class Changelog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log = db.Column(db.Text, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    api_id = db.Column(db.Integer, db.ForeignKey('api.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Changelog %r>' % self.id


user_api_table = db.Table('user_apis', db.Model.metadata,
                          db.Column('id', db.Integer, primary_key=True),
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('api_id', db.Integer, db.ForeignKey('api.id')))
"""
user_nitification_table = db.Table('user_notification', db.Model.metadata,
                          db.Column('id', db.Integer, primary_key=True),
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('changelog_id', db.Integer, db.ForeignKey('changelog.id')),
                          db.Column('read', db.Integer))
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role_name = db.Column(db.String(20), nullable=False, default=u"viewer")
    following_apis = db.relationship('Api', secondary=user_api_table)
    #user_notification = db.relationship('Changelog', secondary=user_nitification_table)

    def __repr__(self):
        return '<User %r>' % self.id


class UserNotify(db.Model):
    __tablename__ = 'user_notification'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    changelog_id = db.Column('changelog_id', db.Integer, db.ForeignKey('changelog.id'))
    read = db.Column('read', db.Integer)
    #changelog = db.relationship(Changelog, backref="memberships")
    user = db.relationship(User, backref="user_notification")


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    api_id = db.Column(db.Integer, db.ForeignKey('api.id'))
    api_url = db.Column(db.String(500))
    feedback_content = db.Column(db.String(500))
    feedback_type = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    has_solved = db.Column(db.Integer)
