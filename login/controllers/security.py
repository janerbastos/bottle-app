import bcrypt
from core import app, views
from core.forms.validate.form import required_field, Form
from bottle import redirect, request
from bson.json_util import dumps
from login.models.auth import User
from bottle_utils.csrf import csrf_protect, csrf_token, csrf_tag
# from core import mongo

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
    password = str.encode(request.forms.get('password'))
    usuario = db.query(User).filter_by(username=username).first()
    if usuario:
        salt = str.encode(usuario.salt)
        hashed = bcrypt.hashpw(password, salt)
        result = True if usuario.hashed == hashed else False
        if result:
            session['user'] = dumps(usuario.to_json())
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
    
    return {'token': request.csrf_token}


@app.route('/register', method='POST')
@views('login/register.html')
@csrf_protect
@csrf_token
def do_register(db):
    
    username = request.forms.get('username')
    confirma_password = request.forms.get('confirma_password')

    for key, value in request.forms.items():
        print(key, ' -> ', value)

    error = required_field(request.forms,
            ['first_name', 'last_name', 'username', 'email', 'password'])

    if error:
        return {'error': error, 'code': 'danger', 'token': request.csrf_token}


    usuario_exist = db.query(User).filter_by(username=username).first()
    if usuario_exist:
        return {'message': 'Usuário exite.', 'code': 'danger', 'token': request.csrf_token}

    form = Form(request.forms, User)
    user = form.save(['first_name', 'last_name', 'username', 'email', 'password'])

    db.add(user)
    return {'message': 'Usuário registrado com sucesso.', 'code': 'success', 'token': request.csrf_token}