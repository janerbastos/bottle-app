from core import app, views
from bottle import template, response


@app.route('/blog')
@views('blog/home.html')
def home(session):
    data = None
    username = session.get('username')
    if username:
        data = {
            "nome": username,
            "title_page": "APP Blog",
        }
        return data
    else:
        response.status = 303
        response.set_header('location', '/?code=403')
        return {}
