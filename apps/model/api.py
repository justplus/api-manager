#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/11'
from apps import db


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