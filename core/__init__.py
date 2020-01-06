import functools
import bottle_session
from bottle import Bottle, jinja2_view
from core.connections.mongo_db import Database

print('\nInicializando modolo principal da aplicação')
app = Bottle()

print('Inicializando componente de conexão com mongo')
mongo = Database().connect()

print('Configutando template de aplicação')
# TEMPLATE_PATH.insert(0, 'templates')
views = functools.partial(jinja2_view, template_lookup=['templates'])

plugin_session = bottle_session.SessionPlugin(cookie_lifetime=120, host='192.168.99.100', password='Redis2019!')

print('Inicializando plugin de session')
app.install(plugin_session)

print('Inicializadno modulos de aplicação')
print('\n')
from core.controllers import staticfiles
from login.controllers import security
from blog.controllers import blog
