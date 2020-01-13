from core import app, views
from core.decorators import login_required
from bottle import template, response, redirect
import json


@app.route('/blog')
@views('blog/home.html')
@login_required
def home(session):
    data = None
    user = session.get('user')
    data = {
        "user": json.loads(user),
        "title_page": "APP Blog",
    }
    return data

