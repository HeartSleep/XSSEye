from flask import Flask

import core
from config import Config

app = Flask(__name__)
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
