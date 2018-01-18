from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as password_context
import re

db = SQLAlchemy()
ma = Marshmallow()

class AddUpdateDelete():   
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


# User

class User(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    # save the hashed password
    hashed_password = db.Column(db.String(120), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def verify_password(self, password):
        return password_context.verify(password, self.hashed_password)

    def check_password_strength_and_hash_if_ok(self, password):
        if len(password) < 8:
            return 'The password is too short', False
        if len(password) > 32:
            return 'The password is too long', False
        if re.search(r'[A-Z]', password) is None:
            return 'The password must include at least one uppercase letter', False
        if re.search(r'[a-z]', password) is None:
            return 'The password must include at least one lowercase letter', False
        if re.search(r'\d', password) is None:
            return 'The password must include at least one number', False
        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None:
            return 'The password must include at least one symbol', False
        self.hashed_password = password_context.encrypt(password)
        return '', True

    def __init__(self, name):
        self.name = name


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor('api.userresource', id='<id>', _external=True)



# Client

class Client(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    @classmethod
    def is_unique(cls, id, name):
        existing_client = cls.query.filter_by(name=name).first()
        if existing_client is None:
            return True
        else:
            if existing_client.id == id:
                return True
            else:
                return False


class ClientSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor('api.clientresource', id='<id>', _external=True)
    messages = fields.Nested('FeatureSchema', many=True, exclude=('client',))


# Area

class Area(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    @classmethod
    def is_unique(cls, id, name):
        existing_area = cls.query.filter_by(name=name).first()
        if existing_area is None:
            return True
        else:
            if existing_area.id == id:
                return True
            else:
                return False


class AreaSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor('api.arearesource', id='<id>', _external=True)
    messages = fields.Nested('FeatureSchema', many=True, exclude=('area',))


# Feature

class Feature(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    client_priority = db.Column(db.Integer, nullable=False)

    # Relationships
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    client = db.relationship('Client', backref=db.backref('features', lazy='dynamic' , order_by='Feature.title'))    
    area_id = db.Column(db.Integer, db.ForeignKey('area.id', ondelete='CASCADE'), nullable=False)
    area = db.relationship('Area', backref=db.backref('features', lazy='dynamic' , order_by='Feature.title'))

    def __init__(self, title, description, target_date, client_priority, client, area):
        self.title = title
        self.description = description
        self.target_date = target_date
        self.client_priority = client_priority
        self.client = client
        self.area = area


class FeatureSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(1))
    description = fields.String(required=True, validate=validate.Length(1))    
    creation_date = fields.DateTime()
    target_date = fields.DateTime()
    client_priority = fields.Integer()
    url = ma.URLFor('api.featureresource', id='<id>', _external=True)

    # relationships
    client = fields.Nested(ClientSchema, only=['id', 'url', 'name'], required=True)
    area = fields.Nested(AreaSchema, only=['id', 'url', 'name'], required=True)

    @pre_load
    def process_client_and_area(self, data):
        client = data.get('client')
        if client:
            if isinstance(client, dict):
                client_id = client.get('id')
            else:
                client_id = client
            client_dict = dict(name=client_id)                
        else:
            client_dict = {}
        data['client'] = client_dict

        area = data.get('area')
        if area:
            if isinstance(area, dict):
                area_id = area.get('id')
            else:
                area_id = area
            area_dict = dict(name=area_id)                
        else:
            area_dict = {}
        data['area'] = area_dict
        return data
