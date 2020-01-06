import bcrypt
from core import app, views
from bottle import redirect, request
from bson.json_util import dumps
from core import mongo

db = mongo.login

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
def do_login(session):
    username = request.forms.get('username')
    password = str.encode(request.forms.get('password'))
    usuario = db['usuario'].find_one({'username': username})
    if usuario:
        salt = str.encode(usuario.get('salt'))
        hashed = bcrypt.hashpw(password, salt)
        result = True if usuario.get('hashed') == hashed else False
        if result:
            session['username'] = usuario.get('username')
            return redirect('/blog')
    return {'message': 'Usuário ou senha podem esta errados.'}

@app.route('/logout')
def logout(session):
    if session.get('username'):
        session.destroy()
    return redirect('login')


@app.route('/register')
@views('login/register.html')
def register():
    return {}


@app.route('/register', method='POST')
@views('login/register.html')
def do_register():
    username = request.forms.get('username')
    usuario_exist = db.usuario.find_one({'username':username})
    if usuario_exist:
        return {'message': 'Usuário exite.', 'code': 'danger'}
    password = str.encode(request.forms.get('password'))
    salt = bcrypt.gensalt(8)
    data = {
        'username': username,
        'hashed': bcrypt.hashpw(password, salt),
        'salt': str(salt, 'utf-8')
    }
    db['usuario'].insert_one(data)
    return {'message': 'Usuário registrado com sucesso.', 'code': 'success'}