from asyncrisk import app, login_manager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {
        'schema': 'asyncrisk'
    }
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    friend_user = db.relationship('Friends', foreign_keys='Friends.user_id')
    friend_friend = db.relationship('Friends', foreign_keys='Friends.friend_id')
    request_user = db.relationship('Requests', foreign_keys='Requests.user_id')
    request_requester = db.relationship('Requests', foreign_keys='Requests.requester_id')

    def __repr__(self):
        return f"Users( '{self.username}', '{self.email}')"


class Friends(db.Model):
    __tablename__ = 'friends'
    __table_args__ = {
        'schema': 'asyncrisk'
    }
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('asyncrisk.users.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('asyncrisk.users.id'))


class Requests(db.Model):
    __tablename__ = 'requests'
    __table_args__ = {
        'schema': 'asyncrisk'
    }
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('asyncrisk.users.id'))
    requester_id = db.Column(db.Integer, db.ForeignKey('asyncrisk.users.id'))