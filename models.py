

from datetime import datetime

from flask import current_app

from flask_sqlalchemy import SQLAlchemy





db = SQLAlchemy()



 


class User(db.Model ):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(100))
    
    email = db.Column(db.String(100), unique=True)

    text = db.Column(db.String(10000) , nullable=True)

    status = db.Column(db.Integer , default=0)

    password = db.Column(db.String(200))






 


class Admin(db.Model ):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(100) )
    
    password = db.Column(db.String(100))

