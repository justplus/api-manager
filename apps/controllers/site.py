#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/10'
from flask import Flask, Blueprint
from flask import render_template, abort, request, session, redirect, url_for
from apps.model.api import Api, Category, Param
from sqlalchemy import or_
import requests, json

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    category_list = Category.query.order_by(Category.id).all()
    api_list = []
    for category in category_list:
        api_list_by_category = Api.query.filter_by(api_category=category.id).all()
        api = dict()
        api['category'] = category.category_name
        api['apis'] = api_list_by_category
        api_list.append(api)
    return render_template('index.html', locals=locals())

@bp.route('/<int:api_id>')
def view(api_id):
    from operator import attrgetter
    api = Api.query.get(api_id)
    if not api:
        abort(404)
    category = api.category.category_name
    api.api_changelog = sorted(api.api_changelog, key=attrgetter('update_time'), reverse=True)
    #api.api_name = api.api_name[(api.api_name.index('=') + 1):]
    return render_template('view.html', locals=locals())

@bp.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        method = request.form['method']
        url = request.form['url']
        auth_string = '&version=1.0&format=json&appkey=KtSNKxk3&access_token=changyanyun'
        try:
            if method.lower() == 'get':
                r = requests.get(url + auth_string, timeout=10)
            else:
                r = requests.post(url + auth_string, timeout=10)
        except Exception,ex:
            return json.dumps({'status_code': 500, 'content': 'internal server error'}, ensure_ascii=False)
        return json.dumps({'status_code': r.status_code, 'content': r.json()}, ensure_ascii=False)

@bp.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        api_list = Api.query.filter(or_(Api.api_description.like('%'+keyword+'%'),Api.api_name.like('%'+keyword+'%'))).all()
        html = u'<table class="pure-table pure-table-bordered api-list"><tbody><tr class="header"><td colspan="4">搜索结果</td></tr>'
        for search_api in api_list:
            html = html + u"""<tr class="list"><td class="td2">
                            <span class="method-get">GET</span>
                            <span class="method-post">POST</span>
                            </td>
                            <td class="td3"><a href="/%s">%s</a></td>
                            <td class="td4">%s</td>
                            <td class="td1"><button class="pure-button pure-button-xsmall pure-button-success">关注</button></td>
                        </tr>""" % (search_api.id, search_api.api_name, search_api.api_description)
        html = html + '</tbody></table>'
        return html

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('logined', None) == True:
            return redirect(url_for('admin.index'))
        return render_template('/login.html')
    else:
        user_name = request.form['user_name']
        password = request.form['password']
        #TODO：将用户名、加密的密码放到数据库
        accounts = [{'test': 'test'}]
        for account in accounts:
            if account.get(user_name, None) == password:
                session['logined'] = True
                return "ok"
        return "wrong"