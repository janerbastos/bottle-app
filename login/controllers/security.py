import bcrypt
from core import app, views
from bottle import redirect, request
from bson.json_util import dumps
from login.models.auth import User
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
def register():
    return {}


@app.route('/register', method='POST')
@views('login/register.html')
def do_register(db):
    username = request.forms.get('username')
    usuario_exist = db.query(User).filter_by(username=username).first()
    if usuario_exist:
        return {'message': 'Usuário exite.', 'code': 'danger'}
    
    first_name = request.forms.get('first_name')
    last_name = request.forms.get('last_name')
    email = request.forms.get('email')
    password = request.forms.get('password')
    confirma_password = request.forms.get('confirma_password')
    salt = bcrypt.gensalt(8)
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email': email,
        'hashed': bcrypt.hashpw(str.encode(password), salt),
        'salt': str(salt, 'utf-8')
    }
    user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            hashed=bcrypt.hashpw(str.encode(password), salt),
            salt=str(salt, 'utf-8')
        )
    db.add(user)
    return {'message': 'Usuário registrado com sucesso.', 'code': 'success'}