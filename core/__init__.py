import bottle_session
from bottle import Bottle, TEMPLATE_PATH

app = Bottle()
TEMPLATE_PATH.insert(0, 'templates')

plugin_session = bottle_session.SessionPlugin(cookie_lifetime=120, password='Redis2019!')

app.install(plugin_session)

from core.controllers import staticfiles
from login.controllers import security
from blog.controllers import blog