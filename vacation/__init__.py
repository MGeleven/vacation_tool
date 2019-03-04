import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.config['SECRET_KEY'] = 'aea6f66f0fcad899e8e8f09335489a18'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from vacation import routes