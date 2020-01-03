from core import app
from bottle import template, response


@app.route('/blog')
def home(session):
    acesso = False
    data = None
    username = session.get('username')
    if username:
        acesso = True
        data = {
            "nome": username,
            "title_page": "APP Blog"
        }
        return template('blog/home', data, acesso=acesso)
    else:
        response.status = 303
        response.set_header('location', '/?acesso=False')
        return None