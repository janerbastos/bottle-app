
from core import app, views
from core.forms.validate.form import required_field, Form
from bottle import redirect, request
from bson.json_util import dumps
from login.models.auth import User
from bottle_utils.csrf import csrf_protect, csrf_token, csrf_tag
from sqlite3 import IntegrityError
# from core import mongo

import datetime

# db = mongo.login

@app.route('/')
@app.route('/<acesso>')
@views('login/login.html')
def login(acesso=True):
    data = {'message': None}
    code = request.params.get('code')
    if code == '403':
        data['message'] = 'Acesso não autorizado'
    return data


@app.route('/', method='POST')
@views('login/login.html')
def do_login(db, session):
    username = request.forms.get('username')
    password = request.forms.get('password')
    usuario = db.query(User).filter_by(username=username).first()
    if usuario:
        result = usuario.check_password(password)
        if result:
            session['user'] = dumps(usuario.to_json())
            usuario.last_login = datetime.datetime.utcnow()
            db.add(usuario)
            return redirect('/blog')
    return {'message': 'Usuário ou senha podem esta errados.'}

@app.route('/logout')
def logout(session):
    if session.get('user'):
        session.destroy()
    return redirect('login')


@app.route('/register')
@views('login/register.html')
@csrf_token
def register():
    data = {
        'first_name': None, 'last_name': None, 'username': None, 'email': None, 'password': None
    }
    return {'token': request.csrf_token, 'data': data, 'error': None}


@app.route('/register', method='POST')
@views('login/register.html')
@csrf_protect
@csrf_token
def do_register(db):
    
    username = request.forms.get('username')
    confirma_password = request.forms.get('confirma_password')

    result = required_field(request.forms,
            ['first_name', 'last_name', 'username', 'email', 'password'])
    
    if result.get('error'):
        return {'error': result.get('error'), 'data': result.get('data'), 'code': 'danger', 'token': request.csrf_token}


    usuario_exist = db.query(User).filter_by(username=username).first()
    if usuario_exist:
        return {'error': result.get('error'), 'data': result.get('data'), 'message': 'Usuário exite.', 'code': 'danger', 'token': request.csrf_token}

    form = Form(request.forms, User)
    user = form.save(['first_name', 'last_name', 'username', 'email', 'password'])
    if not user.check_password(confirma_password):
        return {'error': result.get('error'), 'data': result.get('data'),'message': 'Senha não confirma.', 'code': 'danger', 'token': request.csrf_token}

    usuario_email_exist = db.query(User).filter_by(email=user.email).first()
    if usuario_email_exist:
        return {'error': result.get('error'), 'data': result.get('data'),
            'message': 'Email de usuário já esta sendo usado por outro usuário.', 'code': 'danger', 'token': request.csrf_token}
    
    db.add(user)

    return {'data': None, 'error': None, 'message': 'Usuário registrado com sucesso.', 'code': 'success', 'token': request.csrf_token}