from core import app, views
from bottle import template, response, redirect
import json


@app.route('/blog')
@views('blog/home.html')
def home(session):
    data = None
    user = session.get('user')
    if user:
        data = {
            "user": json.loads(user),
            "title_page": "APP Blog",
        }
        return data
    else:
        response.flash({'message': 'Usuário não autorizado', 'code': 'danger'})
        return redirect('/')
        # response.status = 303
        # response.set_header('location', '/?code=403')
        # return {}
