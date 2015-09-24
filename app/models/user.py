# coding: utf-8
__author__ = 'Stanislav Varnavsky'

from app import db
from flask import g, session
from app.components.tools import Tools


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True)
    key = db.Column(db.String(255))
    token = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    auth = db.Column(db.SmallInteger)
    files = db.relationship('File', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime)
    info = db.Column(db.Text)

    @staticmethod
    def get_current():
        user = g.user
        if user.get_id() is None:
            user = User.anonymous()
        return user

    @staticmethod
    def anonymous():
        name = 'Anonymous'
        email = 'anon@no.email'
        photo = 'https://cdn0.iconfinder.com/data/icons/social-flat-rounded-rects/512/anonymous-128.png'
        return User(name=name, email=email, photo=photo)

    def is_authenticated(self):
        return session.get('authorized')

    def is_active(self):
        return session.get('active')

    def is_anonymous(self):
        return self.email == 'anon@no.email'

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def get_files_count(self):
        count = 0
        for file in self.files:
            count += 1
        return str(count)

    def get_files_size(self, prefix=None):
        bytes = 0
        for file in self.files:
            bytes += file.size
        size = bytes
        if prefix is not None:
            size = round(Tools.size_metric(bytes, prefix), 3)
        return str(size)

    def get_files_dict(self):
        files = {}
        for file in self.files:
            files[file.id] = file.to_json()
        return files

    def __repr__(self):
        return '<User %r>' % (self.name + ' / ' + self.email)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'key': self.key,
            'token': self.token,
            'photo': self.photo,
            'auth': self.auth,
            'last_seen': str(self.last_seen),
            'info': self.info,
            'files': self.get_files_dict(),
            'files_count': self.get_files_count(),
            'files_size': self.get_files_size('megabytes')
        }
