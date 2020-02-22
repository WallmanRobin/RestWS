# coding=utf-8

"""
后台服务初始化配置模块
"""

import logging.config
from datetime import timedelta
from flask import Flask, current_app
from flask_cors import CORS
from flask_session import Session
from os import path
from redis import Redis

from org.rear import ctx
from org.rear.blueprint.Authorization import authorization_bp
from org.rear.blueprint.Authorize import authorize_bp
from org.rear.blueprint.BasicAuth import basicAuth_bp
from org.rear.blueprint.DataTool import datatool_bp
from org.rear.blueprint.Tree import tree_bp
from org.rear.blueprint.Util import util_bp
from org.rear.blueprint.Weixin import weixin_bp
from org.rear.util import cfg

app = Flask(__name__)
app.config['SECRET_KEY'] = cfg.appSecretKey()
app.register_blueprint(weixin_bp, url_prefix='/weixin')
app.register_blueprint(authorize_bp, url_prefix='/authorize')
app.register_blueprint(authorization_bp, url_prefix='/authorization')
app.register_blueprint(basicAuth_bp, url_prefix='/basicAuth')
app.register_blueprint(tree_bp, url_prefix='/tree')
app.register_blueprint(util_bp, url_prefix='/util')
app.register_blueprint(datatool_bp, url_prefix='/datatool')
CORS(app, supports_credentials=True)

session_config = cfg.sessionCfg()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = session_config['session_type']
if app.config['SESSION_TYPE'] == 'filesystem':
    app.config['SESSION_FILE_DIR'] = session_config['session_file_dir']
elif app.config['SESSION_TYPE'] == 'redis':
    app.config['SESSION_REDIS'] = Redis(host=session_config['redis_server'], port=session_config['redis_port'],
                                        password=session_config['secret_key'])
    app.config['SESSION_KEY_PREFIX'] = session_config['session_key_prefix']
t = session_config['life_time']
if t!=-1:
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=t)
Session(app)

ctx.db_engine.dispose()

logging.config.fileConfig(path.join(path.dirname(__file__), 'logging.conf'))

if __name__ == '__main__':
    app.debug = True
    app.run()
