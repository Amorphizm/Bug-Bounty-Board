from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(250))
    creator = db.Column(db.String(50))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    description = db.Column(db.String(250))
    priority = db.Column(db.Integer)
    status = db.Column(db.String(25))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    comments = db.relationship('Comment')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    description = db.Column(db.String(150))
    tickets = db.relationship('Ticket')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # foreign key class lowercase

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    passwd = db.Column(db.String(150))
    f_name = db.Column(db.String(150))
    projects = db.relationship('Project') # relationship class uppercase
