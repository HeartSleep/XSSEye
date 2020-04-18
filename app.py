from flask import Flask

import core
from config import Config


class ReverseProxyWrapper(object):
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.wsgi_app(environ, start_response)


app = Flask(__name__)
app.wsgi_app = ReverseProxyWrapper(app.wsgi_app)
app.config.from_object(Config)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


core.on_init()
core.register_blueprint(app)

app.run(debug=True)
