from bottle import response, redirect
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(session, db=None):
        params={
            'session': session
        }
        
        if db:
            params['db'] = db

        if(session['user']):
            return f(**params)
        else:
            response.flash({'message': 'Usuário não esta autorizado a acessa essa requisição.', 'code': 'danger'})
            return redirect('login')

    return wrapper