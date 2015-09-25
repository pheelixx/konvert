# coding: utf-8
__author__ = 'Stanislav Varnavsky'

from flask import render_template, redirect, session, url_for, request, g, jsonify, send_file
from flask.ext.login import login_user, logout_user, current_user, login_required
from config import OAUTH_CREDENTIALS
from app import app, db, manager
from components.auth import AUTH, twitter, vk, facebook
from components.tools import Tools
from components.document import Document
from models.user import User
from models.file import File
from datetime import datetime
import hashlib, urllib, mimetypes, json, os


@app.route('/fonts/<file>')
def fonts(file):
    filename = 'fonts/' + file
    return redirect(url_for('static', filename=filename))


@app.route('/images/<file>')
def images(file):
    filename = 'images/' + file
    return redirect(url_for('static', filename=filename))


@app.route('/')
def index():
    user = g.user
    if user.get_id() is None:
        user = User.anonymous()
    jsoned = json.dumps({
        'user': user.to_json()
    })
    return render_template('index.html', user=user, view='view/user.html', jsoned=jsoned)


@app.route('/user/<int:id>')
def user(id):
    user = User.get_current()
    if user.is_anonymous() or user.id != id:
        return error_forbidden(error='Have not permissions')
    return render_template('index.html', view='view/user.html', user=user)


@app.route('/file/<int:id>')
def file(id):
    file = File.query.get(id)
    if file is None:
        return error_not_found(error='File not found')
    user = User.get_current()
    if user.is_anonymous() or file.user_id != user.id:
        return error_forbidden(error='Have not permissions')
    settings = file.get_settings()
    selected = settings.keys()[0]
    jsoned = json.dumps({
        'user': user.to_json(),
        'file': file.to_json(),
        'settings': settings,
        'selected': selected,
        'statistics': file.get_statistics()
    })
    return render_template('index.html',
                           view='view/file.html',
                           user=user,
                           file=file,
                           settings=settings,
                           selected=selected,
                           jsoned=jsoned)


@app.route('/download/<int:id>')
def download(id):
    user = User.get_current()
    if user.id == g.user.id:
        file = File.query.get(id)
        if file is not None:
            filename = file.name.encode('cp1251')
            return send_file(file.path, as_attachment=True, attachment_filename=filename)
    return jsonify({'result': 'oops, fail'})


@app.route('/upload', methods=['POST'])
def upload():
    return jsonify(Tools.upload())


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    key = False
    deleted = False
    if 'key' in request.values:
        key = request.values['key']
        user = User.query.filter_by(key=key).first()
        file = File.query.filter_by(id=id).first()
        if user is not None and file is not None and file.user_id == user.id:
            db.session.delete(file)
            db.session.commit()
            deleted = True
    result = {
        'key': key,
        'id': id,
        'deleted': deleted
    }
    return jsonify(result)


@app.route('/conv/<int:id>', methods=['POST'])
def conv(id):
    settings = {}
    for key, value in request.values.items():
        settings[key] = value
        if value.isdigit():
            settings[key] = int(value)
        if value == 'true':
            settings[key] = True
        if value == 'false':
            settings[key] = False
    extension = settings['extension']
    file = File.query.get(id)
    path = file.path
    basename = Tools.get_basename(file.name)
    new_name = (basename + '.' + extension).encode('utf-8')
    document = Document(path)
    properties = document.get_export_options(extension)
    properties['FilterData'] = settings
    document.set_properties(properties)
    # return jsonify({
    #     'id': id,
    #     'settings': settings,
    #     'options': options,
    #     'export_options': document.get_export_options(extension),
    #     'arguments': dir(document.arguments),
    #     'statistics': document.get_statistics(),
    #     'get_settings': file.get_settings()
    # })
    new = path + '.' + extension
    save = document.save(new)
    if save is False:
        return jsonify({
            'error': 'File not saved'
        })
    type = mimetypes.guess_type(urllib.pathname2url(new_name))
    model = File.query.filter_by(path=new).first()
    if model is None:
        model = File()
    model.user_id = g.user.id
    model.name = new_name.decode('utf-8')
    model.path = new
    model.size = os.path.getsize(new)
    model.type = type[0]
    model.extension = extension
    db.session.add(model)
    db.session.commit()
    return jsonify({
        'save': save,
        'name': new_name,
        'url': '/download/' + str(model.id),
        'type': type[0],
        'path': new,
        'properties': properties
    })

@app.route('/convert', methods=['POST'])
def convert():
    upload = Tools.upload()
    path = upload['path']
    basename = Tools.get_basename(upload['name'])
    new_name = (basename + '.pdf').encode('utf-8')
    document = Document(upload['path'])
    new = path + '.pdf'
    save = document.save(new)
    user_id = 1
    type = mimetypes.guess_type(urllib.pathname2url(new_name))
    model = File(user_id=user_id,
                 name=new_name.decode('utf-8'),
                 path=new,
                 type=type[0])
    db.session.add(model)
    db.session.commit()
    return jsonify({
        'save': save,
        'name': new_name,
        'url': '/download/' + str(model.id),
        'type': type[0],
        'path': new
    })


@manager.user_loader
def load_user(id):
    user = User.query.get(id)
    return user


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/login/twitter', methods=['GET', 'POST'])
def login_twitter():
    return twitter.authorize(callback=url_for('authorized'))


@app.route('/login/vk')
def login_vk():
    url = 'authorized_with_vk'
    next = request.args.get('next') or request.referrer or None
    callback = url_for(url, _external=True, next=next)
    return vk.authorize(callback=callback)


@app.route('/login/fb')
def login_facebook():
    url = 'authorized_with_facebook'
    next = request.args.get('next') or request.referrer or None
    callback = url_for(url, _external=True, next=next)
    return facebook.authorize(callback=callback)


@app.route('/authorized/facebook')
@facebook.authorized_handler
def authorized_with_facebook(response):
    result = {'auth': False}
    if response is not None:
        access_token = response['access_token']
        # expires = response['expires']
        session['facebook_token'] = (
            access_token,
            OAUTH_CREDENTIALS['facebook']['secret']
        )
        get = facebook.get('me?fields=id,name,picture,email')
        status = get.status
        result['get_status'] = status
        if status == 200:
            data = get.data
            user = User.query.filter_by(email=data['email']).first()
            if user is None:
                result['user_status'] = 'new'
                user = User(
                    name=data['name'],
                    email=data['email'],
                    key=Tools.generate_hash(data),
                    token=access_token,
                    photo=data['picture']['data']['url'],
                    auth=AUTH['facebook'],
                    last_seen=str(datetime.utcnow()),
                    info=json.dumps(data)
                )
                db.session.add(user)
                db.session.commit()
            else:
                result['user_status'] = 'old'
                equal = True
                new = {
                    'name': data['name'],
                    'token': access_token,
                    'photo': data['picture']['data']['url']
                }
                for key, value in new.iteritems():
                    attr = getattr(user, key)
                    if attr != value:
                        setattr(user, key, value)
                        equal = False
                if not equal:
                    result['user_status'] = 'updated'
                    db.session.add(user)
                    db.session.commit()
            result['user'] = {
                'name': user.name,
                'email': user.email,
                'key': user.key,
                'photo': user.photo,
                'info': user.info
            }
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            session['authorized'] = True
            session['active'] = True
            session['anonymous'] = False
            result['auth'] = login_user(user, remember=remember_me)
    return redirect(url_for('index'))


@app.route('/authorized/vk')
@vk.authorized_handler
def authorized_with_vk(response):
    result = {'auth': False}
    if response is not None:
        access_token = response['access_token']
        # expires = response['expires']
        user_id = str(response['user_id'])
        email = str(response['email'])
        session['vk_token'] = (
            access_token,
            OAUTH_CREDENTIALS['vk']['secret']
        )
        method = 'method/users.get?uids=' + user_id + '&fields=uid,first_name,last_name,nickname,photo'
        get = vk.get(method)
        status = get.status
        result['get_status'] = status
        if status == 200:
            data = get.data['response'][0]
            user = User.query.filter_by(email=email).first()
            name = data['first_name'] + ' ' + data['last_name']
            now = str(datetime.utcnow())
            phrase = email + data['first_name'] + name + now
            key = hashlib.sha384(phrase).hexdigest()
            if user is None:
                result['user_status'] = 'new'
                user = User(
                    name=name,
                    email=email,
                    key=key,
                    token=access_token,
                    photo=data['photo'],
                    auth=AUTH['vk'],
                    last_seen=now,
                    info=json.dumps(data)
                )
                db.session.add(user)
                db.session.commit()
            else:
                result['user_status'] = 'old'
                equal = True
                new = {
                    'name': name,
                    'token': access_token,
                    'photo': data['photo']
                }
                for key, value in new.iteritems():
                    attr = getattr(user, key)
                    if attr != value:
                        setattr(user, key, value)
                        equal = False
                if not equal:
                    result['user_status'] = 'updated'
                    db.session.add(user)
                    db.session.commit()
            result['user'] = {
                'name': user.name,
                'email': user.email,
                'key': user.key,
                'photo': user.photo,
                'info': user.info
            }
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            session['authorized'] = True
            session['active'] = True
            session['anonymous'] = False
            result['auth'] = login_user(user, remember=remember_me)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(403)
def error_forbidden(error):
    return render_template('error/403.html', error=error), 403


@app.errorhandler(404)
def error_not_found(error):
    return render_template('error/404.html', error=error), 404


@app.errorhandler(500)
def error_internal(error):
    db.session.rollback()
    return render_template('error/500.html', error=error), 500
