from core import app
import os

if __name__ == '__main__':
    if os.environ.get('APP_LOCATION') == 'heroku':
        app.run(server='paste', host='0.0.0.0', port=int(os.environ.get('PORT', 500)))
    else:
        app.run(host='localhost', port=8080, debug=True, reloader=True)