from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as password_context
from models import db, ma

class Feature(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    client_priority = db.Column(db.Integer, nullable=False)

    # Relationships
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    client = db.relationship('Client', backref=db.backref('features', lazy='dynamic' , order_by='Feature.feature'))    
    area_id = db.Column(db.Integer, db.ForeignKey('area.id', ondelete='CASCADE'), nullable=False)
    area = db.relationship('Area', backref=db.backref('features', lazy='dynamic' , order_by='Feature.feature'))

    def __init__(self, title, description, target_date, client_priority, client, area):
        self.title = title
        self.description = description
        self.target_date = target_date
        self.client_priority = client_priority
        self.client = client
        self.area = area


class MessageSchema(ma.Schema):
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
    def process_client(self, data):
        client = data.get('client')
        if client:
            if isinstance(client, dict):
                client_name = client.get('name')
            else:
                client_name = client
            client_dict = dict(name=client_name)                
        else:
            client_dict = {}
        data['client'] = client_dict
        return data


    @pre_load
    def process_area(self, data):
        area = data.get('area')
        if area:
            if isinstance(area, dict):
                area_name = area.get('name')
            else:
                area_name = area
            area_dict = dict(name=area_name)                
        else:
            area_dict = {}
        data['area'] = area_dict
        return data