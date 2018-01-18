from flask import Flask, Blueprint
from flasgger import Swagger
from .models import db

site = Blueprint('site', __name__)

@site.route("/")
def index():
    html = "<h1>Hello world!</h1> <h3>The features api is running...</h3>"
    return html

def create_app(config_filename, debug=True):
    app = Flask(__name__)
    Swagger(app)
    app.debug = debug
    app.config.from_object(config_filename)
    
    # from .models import db
    db.init_app(app)

    app.register_blueprint(site)
    return app