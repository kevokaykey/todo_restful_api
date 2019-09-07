from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from app import *

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\KK\\Documents\\python\\api\\todo.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Todo(db.Model):
     id = db.Column(db.Integer, primary_key="True")
     text= db.Column(db.String(50))  
     complete = db.Column(db.Boolean)
     user_id = db.Column(db.Integer)