#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/12'
from flask import Flask, Blueprint
from flask import render_template, abort, request, redirect, url_for
from apps.model.api import Api, Category, Param, Changelog
from datetime import *
from apps import db, ext
from apps.ext.login import require_login
import json

bp = Blueprint('admin', __name__)

@bp.route('/')
@require_login()
def index():
    category_list = Category.query.order_by(Category.id).all()
    api_list = []
    for category in category_list:
        api_list_by_category = Api.query.filter_by(api_category=category.id).all()
        api = dict()
        api['category'] = category.category_name
        api['apis'] = api_list_by_category
        api_list.append(api)
    return render_template('admin.html', locals=locals())

@bp.route('/add', methods=['GET', 'POST'])
@require_login()
def add():
    if request.method == 'GET':
        category_list = Category.query.all()
        return render_template('add.html', locals=locals())
    elif request.method == 'POST':
        params = json.loads(request.form['params'])
        api = Api(
            api_name=request.form['name'],
            api_description=request.form['description'],
            api_format=request.form['format'],
            api_method=request.form['method'],
            api_auth=1 if str(request.form['auth']).lower() == 'true' else 0,
            api_notice=request.form['notice'],
            api_return=request.form['return'],
            api_category=request.form['category']
        )

        for p in params:
            param = Param(
                param_name=p['name'],
                param_description=p['description'],
                param_must=1 if str(p['must']).lower() == 'true' else 0,
                param_type=p['type'],
                param_default=p['default']
            )
            api.api_params.extend([param])

        changelog = Changelog(
            log=u'首次提交',
            update_time=datetime.now()
        )
        api.api_changelog.extend([changelog])
        db.session.add(api)
        db.session.commit()
        return "ok"

@bp.route('/edit/<int:api_id>', methods=['GET', 'POST'])
@require_login()
def edit(api_id):
    if request.method == 'GET':
        api = Api.query.get(api_id)
        if not api:
            abort(404)
        category = api.category.category_name
        #api.api_name = api.api_name[(api.api_name.index('=') + 1):]
        category_list = Category.query.all()
        j_param = []
        for p in api.api_params:
            j_param.append({
                'name': p.param_name,
                'description': p.param_description,
                'must': p.param_must,
                'type': p.param_type,
                'default': p.param_default,
            })
        param_json = json.dumps(j_param, ensure_ascii=False)
        return render_template('edit.html', locals=locals())
    elif request.method == 'POST':
        api = Api.query.get(api_id)
        api.api_description = request.form['description']
        api.api_format = request.form['format']
        api.api_method = request.form['method']
        api.api_auth = 1 if str(request.form['auth']).lower() == 'true' else 0
        api.api_notice = request.form['notice']
        api.api_return = request.form['return']
        api.api_category = request.form['category']
        api.api_test = request.form['test']
        params = json.loads(request.form['params'].replace('+', ''))

        tmp_params = []
        for p in params:
            param = Param(
                param_name=p['name'],
                param_description=p['description'],
                param_must=1 if str(p['must']).lower() == 'true' else 0,
                param_type=p['type'],
                param_default=p['default']
            )
            tmp_params.append(param)
        api.api_params = tmp_params

        if(request.form['changelog']):
            changelog = Changelog(
                log=request.form['changelog'],
                update_time=datetime.now()
            )
            api.api_changelog.extend([changelog])

        db.session.commit()
        return "ok"


@bp.route('/delete', methods=['POST'])
@require_login()
def delete():
    api_id = request.form['api_id']
    api = Api.query.get(api_id)
    db.session.delete(api)
    db.session.commit()
    return "ok"