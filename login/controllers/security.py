from core import app
from bottle import template, redirect, request

@app.route('/')
@app.route('/<acesso>')
def login(acesso=True):
    acesso = request.params.get('acesso')
    return template('login/login', acesso=acesso)


@app.route('/', method='POST')
def do_login(session):
    session['username'] = 'Janer Bastos de Melo'
    return redirect('blog')

