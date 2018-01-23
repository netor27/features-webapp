from flask import Flask, Blueprint
from flasgger import Swagger
from flask_restful import Api
from web.db import db
from web.resources import *
from web.site import site


def create_app(config_filename, debug=True):
    app = Flask(__name__, static_url_path='/static')
    Swagger(app)
    app.debug = debug
    app.config.from_object(config_filename)    
    db.init_app(app)
    app.register_blueprint(site)
    api_bp = _create_api_blueprint()
    app.register_blueprint(api_bp, url_prefix='/api')
    return app


def _create_api_blueprint():
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)
    api.add_resource(AreaListResource, '/areas/')
    api.add_resource(AreaResource, '/areas/<int:id>')
    api.add_resource(ClientListResource, '/clients/')
    api.add_resource(ClientResource, '/clients/<int:id>')
    api.add_resource(FeatureListResource, '/features/')
    api.add_resource(FeatureResource, '/features/<int:id>')
    api.add_resource(UserListResource, '/users/')
    api.add_resource(UserResource, '/users/<int:id>')
    api.add_resource(UserLoginResource, '/users/<string:name>')
    
    return api_bp
