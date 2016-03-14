#!/usr/bin/env python
# coding=utf-8
from datetime import datetime
from apps.ext.login import require_login

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/10'
from flask import Flask, Blueprint, get_template_attribute
from flask import render_template, abort, request, session, redirect, url_for
from apps.model.api import Api, Category, Param, User, UserNotify, Changelog, Feedback
from apps import db
from sqlalchemy import or_, func, desc, asc
from sqlalchemy import and_
import requests
import json

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    api_list = []
    following = {}
    category_list = Category.query.order_by(Category.id).all()
    for category in category_list:
        api_list_by_category = Api.query.filter_by(api_category=category.id).all()
        follow_list = None
        if session.get('login_name', None):
            user = User.query.filter(User.login_name == session['login_name']).first()
            if user:
                follow_list = user.following_apis
        api = dict()
        api['category'] = category.category_name
        api['apis'] = api_list_by_category
        for _api in api_list_by_category:
            _api.__setattr__('followed', (_api in follow_list) if follow_list else False)
        api_list.append(api)
    return render_template('index.html', locals=locals())

@bp.route('/introduction')
def introduction():
    return render_template('introduction.html')

@bp.route('/guide')
def guide():
    return render_template('guide.html')

@bp.route('/changelog')
def changelog():
    return render_template('changelog.html')

@bp.route('/<int:api_id>')
def view(api_id):
    from operator import attrgetter
    api = Api.query.get(api_id)
    if not api:
        abort(404)
    category = api.category.category_name
    api.api_changelog = sorted(api.api_changelog, key=attrgetter('update_time'), reverse=True)
    #api.api_name = api.api_name[(api.api_name.index('=') + 1):]
    #浏览量+1
    if not api.api_view_count:
        api.api_view_count = 1
    else:
        api.api_view_count += 1
    db.session.commit()
    return render_template('view.html', locals=locals())

@bp.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        method = request.form['method']
        url = request.form['url']
        #不指定http?
        if not url.startswith("http://"):
            url = "http://" + url
        auth_string = 'xxxx'
        try:
            if method.lower() == 'get':
                r = requests.get(url + auth_string, timeout=10)
            else:
                r = requests.post(url + auth_string, timeout=10)
        except Exception, ex:
            return json.dumps({'status_code': 500, 'content': 'internal server error'}, ensure_ascii=False)
        try:
            return json.dumps({'status_code': r.status_code, 'content': r.json()}, ensure_ascii=False)
        except Exception, ex:
            return json.dumps({'status_code': 500, 'content': 'invalid exception'})

@bp.route('/search/<string:keyword>')
def search(keyword):
    api_list = Api.query.filter(or_(Api.api_description.like('%'+keyword+'%'),Api.api_name.like('%'+keyword+'%'))).all()
    follow_list = None
    if session.get('login_name', None):
        user = User.query.filter(User.login_name == session['login_name']).first()
        if user:
            follow_list = user.following_apis
    for _api in api_list:
        _api.__setattr__('followed', (_api in follow_list) if follow_list else False)
    return render_template('search.html', locals=locals())


@bp.route('/follow', methods=['POST'])
def follow():
    if request.method == 'POST':
        api_id = request.form['api_id']
        user_id = request.form['user_id']
        if int(user_id) == -1:
            return "login needed"
        api = Api.query.get(api_id)
        user = User.query.get(user_id)
        #判断是加关注还是取消关注
        if Api.query.filter(api in user.following_apis).first():
            user.following_apis.remove(api)
            api.api_collect_count -= 1
            db.session.commit()
            return "uok"
        else:
            if api and user:
                user.following_apis.append(api)
                api.api_collect_count += 1
                db.session.commit()
                return "ok"
            else:
                return "wrong"

@bp.route('/notification')
@require_login()
def notify():
    user = User.query.get(session['user_id'])
    notification_list = db.session.query(UserNotify, Api, Changelog).join(Changelog, UserNotify.changelog_id == Changelog.id).\
            join(Api, Api.id == Changelog.api_id).filter(UserNotify.user_id == user.id).order_by(desc(UserNotify.id)).all()
    db.session.close()
    #全部置为已读
    notification = UserNotify.query.filter(UserNotify.user_id == user.id).order_by(desc(UserNotify.id)).all()
    for n in notification:
        if n.read == 0:
            n.read = 1
    db.session.commit()
    session['notification'] = 0
    session.modified = True
    return render_template('/notification.html', locals=locals())

@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'GET':
        if not session.get('user_id', None):
            return redirect(url_for('site.login'))
        feedback_list = db.session.query(Feedback, Api, User).join(Api, Feedback.api_id == Api.id).\
            join(User, Feedback.user_id == User.id).filter(Feedback.feedback_type == 1).\
            order_by(asc(Feedback.has_solved)).order_by(desc(Feedback.create_time)).all()
        return render_template('feedback.html', locals=locals())
    else:
        feed_type = request.form['feed_type']
        if int(feed_type) == 0:
            feed_content = request.form['feed_content']
            feedback = Feedback(
                user_id=session.get('user_id', None),
                feedback_content=feed_content,
                feedback_type=0,
                has_solved=0
            )
            db.session.add(feedback)
            db.session.commit()
            return "ok"
        elif int(feed_type) == 1:
            feedback = Feedback(
                user_id=session.get('user_id', None),
                feedback_content=request.form['feed_content'],
                api_id=request.form['api_id'],
                api_url=request.form['api_url'],
                feedback_type=1,
                has_solved=0
            )
            db.session.add(feedback)
            db.session.commit()
            return "ok"
        elif int(feed_type) == -1:
            feedback = Feedback.query.filter(Feedback.id==request.form['id']).first()
            if feedback:
                feedback.has_solved = 1
                db.session.commit()
                return "ok"
            return "wrong"



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('login_name', None):
            return redirect(url_for('admin.index'))
        return render_template('/login.html')
    else:
        login_name = request.form['user_name']
        password = request.form['password']
        user = User.query.filter(and_(User.login_name == login_name, User.password == password)).first()
        if user:
            #获取关注的接口更新数量
            notify_count = db.session.query(func.count(UserNotify.id)).filter(and_(UserNotify.user_id == user.id, UserNotify.read == 0)).first()
            session['notification'] = '99+' if notify_count[0] > 99 else notify_count[0]
            session['user_id'] = user.id
            session['login_name'] = user.login_name
            session['role_name'] = user.role_name
            return user.role_name
        return "wrong"

@bp.route('/logout')
@require_login()
def logout():
    session['user_id'] = None
    session['login_name'] = None
    session['role_name'] = None
    return redirect(url_for('site.index'))


@bp.route('/rlegister', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if session.get('login_name', None):
            return redirect(url_for('admin.index'))
        return render_template('/register.html')
    else:
        login_name = request.form['user_name']
        password = request.form['password']
        user = User(
            login_name=login_name,
            password=password,
            role_name='viewer'
        )
        try:
            db.session.add(user)
            db.session.commit()
            #session['logined'] = True
            #session['login_name'] = login_name
            user = User.query.filter(and_(User.login_name == login_name, User.password == password)).first()
            session['user_id'] = user.id
            session['login_name'] = user.login_name
            session['role_name'] = user.role_name
            return user.role_name
        except Exception, ex:
            print str(ex)
            return "wrong"


def __del__(self):
    db.session.close()
