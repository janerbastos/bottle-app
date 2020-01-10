import functools
import bottle_session
from bottle import Bottle, jinja2_view
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from bottle_utils.flash import message_plugin

#from core.connections.mongo_db import Database

Base = declarative_base()

print('\nInicializando modolo principal da aplicação')
app = Bottle()
app.config.load_config('settings.conf')

# print('Inicializando da conexão com mongo')
# mongo = Database().connect()

print('Inicialização, SQLAlchemy com a função create_engine')
engine = create_engine('sqlite:///database.db', echo=True)

print('Configutando template de aplicação')
# TEMPLATE_PATH.insert(0, 'templates')
views = functools.partial(jinja2_view, template_lookup=['templates'])

print('Inicializando plugin Bottle Session')
plugin_session = bottle_session.SessionPlugin(cookie_lifetime=120, host='localhost', password='Redis2019!')
app.install(plugin_session)

print('Inicializando serviço de mensagem flash')
app.install(message_plugin)

print('Inicializando plugin SQLAlchemy')
plugin_sqlalchemy = sqlalchemy.Plugin(
    engine,
    Base.metadata,
    keyword='db',
    create=True,
    commit=True,
    use_kwargs=False
)
app.install(plugin_sqlalchemy)

print('Inicializadno modulos de aplicação')
print('\n')
from core.controllers import staticfiles
from login.controllers import security
from blog.controllers import blog
