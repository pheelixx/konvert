# coding: utf-8
__author__ = 'Stanislav Varnavsky'

import subprocess
import time
from config import ALLOWED_EXTENSIONS, UPLOAD_PATH
from flask import g, request
import hashlib, os, random
from datetime import datetime
from app import db
from app.models.file import File
from settings import Settings

class Tools:
    def __init__(self):
        pass

    @staticmethod
    def call(command, return_html=True, show_exec_time=True):
        if type(command).__name__ == 'list':
            command = ' '.join(command)
        start_time = time.time()
        pipe = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        output = pipe.stdout.read()
        if show_exec_time:
            delta = time.time() - start_time
            output += "Execution time: %s seconds" % round(delta, 1)
        if return_html:
            output = '<pre>' + output + '</pre>'
        return output

    @staticmethod
    def get_extension(file):
        return os.path.splitext(file)[1][1:]

    @staticmethod
    def get_basename(file):
        return os.path.splitext(file)[0]

    @staticmethod
    def is_allowed_file(file):
        extension = Tools.get_extension(file).lower()
        return extension in ALLOWED_EXTENSIONS

    @staticmethod
    def upload():
        key = False
        if 'key' in request.values:
            key = request.values['key']
        user_defined = g.user is not None and g.user.is_authenticated() and g.user.key == key
        if not user_defined:
            return {
                'error': 'User not defined'
            }
        file = request.files['file']
        type = file.mimetype
        name = file.filename
        extension = os.path.splitext(name)[1][1:]
        if type in Settings.extensions:
            extension = Settings.extensions[type]
        user_id = g.user.id
        phrase = name.encode('utf-8') + datetime.now().isoformat()
        hash = hashlib.md5(phrase).hexdigest()
        directory = os.path.join(UPLOAD_PATH, str(user_id))
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = os.path.join(directory, hash) + '.' + extension
        file.save(path)
        size = os.path.getsize(path)
        model = File.query.filter_by(path=path).first()
        if model is None:
            model = File()
        model.user_id = user_id
        model.name = name,
        model.path = path,
        model.type = type,
        model.size = size,
        model.created_at = datetime.utcnow(),
        model.extension = extension
        db.session.add(model)
        db.session.commit()
        return {
            'user_id': g.user.id,
            'auth': user_defined,
            'name': name,
            'path': path,
            'type': type,
            'id': model.id,
            'size': model.size
        }


    @staticmethod
    def generate_hash(phrases):
        phrase = str(datetime.utcnow())
        for item in phrases:
            phrase += str(item)
        key384 = hashlib.sha384(phrase).hexdigest()
        rand = str(random.randint(1, 16777216))
        return hashlib.md5(key384 + rand).hexdigest()

    @staticmethod
    def size_metric(bytes, prefix):
        fmt = str(prefix[0]).lower()
        formats = ['g', 'm', 'k', 'b']
        for current in formats:
            bytes /= 1024.0
            if fmt == current:
                break
        return bytes
