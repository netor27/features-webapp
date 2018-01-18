from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as password_context
import re
from models import db, ma

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