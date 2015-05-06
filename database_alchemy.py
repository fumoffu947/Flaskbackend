from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import app

db = SQLAlchemy(app)

class UserPas(db.Model):
    #__tablename__ = "UserPas"
    id_u = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    pasword = db.Column(db.Text)

    def __init__(self,id_u,username,pasword):
        self.id_u = id_u
        self.username = username
        self.pasword = pasword

    #def login():

class Users(db.Model):
    #__table__ = Users
    id_u = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    lastname = db.Column(db.Text)
    epost = db.Column(db.Text)
    profilepic = db.Column(db.Text)
    number_of_paths = db.Column(db.Integer)
    number_of_steps = db.Column(db.Integer)
    length_went = db.Column(db.Integer)

    def addUser(name_in,lastname_in,epost_in,profilepic_in,username_in,pasword_in):
        newUser = Users(name=name_in,lastname=lastname_in,epost=epost_in,profilepic=profilepic_in, number_of_paths=0,number_of_steps=0,length_went=0)
        newUnserPas = UserPas(newUser.id_u,username_in,pasword_in)
        db.session.add(newUser)
        db.session.add(newUserPas)
        sb.session.commit()

    #def getUser():

class Friends(db.Model):
    #__table__ = Friends
    id = db.Column(db.Integer, primary_key=True)
    id_u = db.Column(db.Integer)
    id_u_friend = db.Column(db.Integer)

    #def getFriends():

class Posts(db.Model):
    #__table__ = Posts
    id_p = db.Column(db.Integer, primary_key=True)
    id_u = db.Column(db.Integer)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    photo_path_list = db.Column(db.Text)
    position_list = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

    def getUserPost(id_u_in):
        posts = Posts.query.filter_by(id_u=id_u_in).all().order_by(model.Posts.timestamp.desc())
    #def getUserFlow():

    #def postPath():

class Comments(db.Model):
    #__table__ = Comments
    id_c = db.Column(db.Integer, primary_key=True)
    id_p = db.Column(db.Integer)
    id_u = db.Column(db.Integer)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    
    #def postComment():
