#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '2014/10/10'
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    global db
    db = SQLAlchemy(app)
    db.init_app(app)
    register_routes(app)
    register_error_handler(app)
    register_logger(app)
    return app


def register_routes(app):
    from controllers import site, admin
    app.register_blueprint(site.bp, url_prefix='')
    app.register_blueprint(admin.bp, url_prefix='/admin')


def register_error_handler(app):
    @app.errorhandler(400)
    def page_400(error):
        return render_template("error/400.html"), 400

    @app.errorhandler(403)
    def page_403(error):
        return render_template("error/403.html"), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template("error/404.html"), 404

    @app.errorhandler(405)
    def page_405(error):
        return render_template("error/405.html"), 405

    @app.errorhandler(500)
    def page_500(error):
        return render_template("error/500.html"), 500


def register_logger(app):
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('apidoc.log', 'a', 1*1024*1024, 10)
        file_handler.setFormatter(
            logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            )
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('apidoc startup')

db = None
app = create_app()
