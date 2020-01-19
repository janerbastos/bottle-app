
from core import app, views
from login.forns import LoginForm, ChangePasswordForm
from core.decorators import login_required
from bottle import redirect, request, response
from login.models.auth import User
from bottle_utils.csrf import csrf_protect, csrf_token, csrf_tag
# from core import mongo

import datetime, json


# db = mongo.login

@app.route('/')
@app.route('/<acesso>')
@views('login/login.html')
def login(acesso=True):
    data = request.message if request.message else {'message': None, 'code': None}
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
            session['user'] = json.dumps(usuario.to_json())
            usuario.last_login = datetime.datetime.utcnow()
            db.add(usuario)
            return redirect('/blog')
    return {'message': 'Usuário ou senha podem esta errados.', 'code': 'warning'}


@app.route('/logout')
@login_required
def logout(session):
    if session.get('user'):
        session.destroy()
    response.flash({'message': 'Sessão encerrada com sucesso', 'code': 'success'})
    return redirect('login')


@app.route('/register')
@views('login/register.html')
@csrf_token
def register():
    form = LoginForm(request.forms or None)
    data = request.message if request.message else {'message': None, 'code': None}
    data.update({'token': request.csrf_token, 'form': form, })
    return data


@app.route('/register', method='POST')
@views('login/register.html')
@csrf_protect
@csrf_token
def do_register(db):
    
    confirma_password = request.forms.get('confirma_password')
    form = LoginForm(request.forms)
    token = request.csrf_token
    
    usuario_exist = db.query(User).filter_by(username=form.data.get('username')).first()
    if usuario_exist:
        return {'form': form, 'message': 'Usuário exite.', 'code': 'danger', 'token': token}

    email_exist = db.query(User).filter_by(email=form.data.get('email')).first()
    if email_exist:
        return {'form': form, 'message': 'Email já esta sendo usado.', 'code': 'danger', 'token': token}

    if form.is_valid():

        user = form.to_model()
        if not user.check_password(confirma_password):
            return {'form': form, 'message': 'Senha não confirma.', 'code': 'danger', 'token': token}
        db.add(user)
        response.flash({'message': 'Usuário registrado com sucesso', 'code': 'success'})
        return redirect('/register')

    return {'form': form, 'message': 'Corrija os erros e tente novamente', 'code': 'danger', 'token': token}


@app.route('/change_password')
@views('login/change_password.html')
@login_required
@csrf_token
def change_password(session):
    form = ChangePasswordForm(request.forms or None)
    data = request.message if request.message else {'message': None, 'code': None}
    data.update({'token': request.csrf_token, 'form': form, })
    return data


@app.route('/change_password', method='POST')
@views('login/change_password.html')
@login_required
@csrf_protect
@csrf_token
def do_change_password(db, session):
    token = request.csrf_token
    form = ChangePasswordForm(request.forms or None)
    if form.is_valid():
        user_session = json.loads(session.get('user'))
        if form.data.get('new_password') == form.data.get('confirma_password'):
            new_password = form.data.get('new_password')
            user = db.query(User).filter_by(username=user_session.get('username')).first()
            user.change_password(new_password)
            db.add(user)
            response.flash({'message': 'Senha auterada com sucesso', 'code': 'success'})
            return redirect('/change_password')
        else:
            return {'form': form, 'message': 'Senha não confirma', 'code': 'warning', 'token': token}
    return {'form': form, 'message': 'Corrija os erros e tente novamente', 'code': 'danger', 'token': token}
