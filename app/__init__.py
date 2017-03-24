#!/usr/bin/env python3

from flask import Flask 
from config import config

from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap 

db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app(cfg):
    app = Flask(__name__)
    app.config.from_object(config[cfg])

    db.init_app(app)
    bootstrap.init_app(app)

    return app