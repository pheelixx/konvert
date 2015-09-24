# coding: utf-8
__author__ = 'Stanislav Varnavsky'

from app import db
from app.components.settings import Settings

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.Text)
    path = db.Column(db.String(64), unique=True)
    size = db.Column(db.Integer)
    type = db.Column(db.String(255))
    extension = db.Column(db.String(64))
    created_at = db.Column(db.DateTime)

    def get_metric_size(self, prefix):
        from app.components.tools import Tools
        size = round(Tools.size_metric(self.size, prefix), 3)
        return str(size)

    def get_source(self):
        return {
            'Name': self.name,
            'MIME-type': self.type,
            'Size': self.get_metric_size('megabytes') + ' MB',
            'Extension': self.extension
        }

    def get_settings_formats(self):
        formats = []
        extension = self.extension
        routes = Settings.convert_routes
        if extension in routes:
            formats = routes[extension].keys()
        return formats

    def get_settings(self):
        from app.components.document import Document
        from app.components.image import Image
        settings = {}
        extension = self.extension
        routes = Settings.convert_routes
        if extension in routes:
            options = routes[extension]
            for key, value in options.iteritems():
                settings[key] = value(self.path).get_export_options(key)
        return settings

    def get_statistics(self):
        from app.components.document import Document
        return Document(self.path).get_statistics()

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'path': self.path,
            'size': self.size,
            'type': self.type,
            'extension': self.extension,
            'created_at': str(self.created_at)
        }
