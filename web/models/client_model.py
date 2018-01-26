from marshmallow import Schema, fields, pre_load
from marshmallow import validate

from web.models import AddUpdateDelete
from web.db import db, ma


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
    #features = fields.Nested('FeatureSchema', many=True, exclude=('client',))
