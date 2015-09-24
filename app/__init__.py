# coding: utf-8
__author__ = 'Stanislav Varnavsky'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.babel import Babel
from components.momentjs import MomentJS


app = Flask(__name__)
app.debug = True
app.config.from_object('config')
app.jinja_env.globals['moment_js'] = MomentJS
db = SQLAlchemy(app)
mail = Mail(app)
babel = Babel(app)

manager = LoginManager()
manager.init_app(app)
manager.login_view = 'login'

from app import views
from models import file, user

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(filename='log/site.log',
                                       mode='a',
                                       maxBytes=1 * 1024 * 1024,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Site start up!')
