from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from web.helpers import PaginationHelper
from web.models import Area, AreaSchema
from web.resources import AuthRequiredResource
from web.status import status
from web.db import db


area_schema = AreaSchema()

class AreaResource(AuthRequiredResource):
    def get(self, id):
        area = Area.query.get_or_404(id)
        result = area_schema.dump(area).data
        return result

    def patch(self, id):
        area = Area.query.get_or_404(id)
        area_dict = request.get_json()
        if not area_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = area_schema.validate(area_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if 'name' in area_dict:
                area_name = area_dict['name']
                if Area.is_unique(id=id, name=area_name):
                    area.name = area_name
                else:
                    response = {
                        'error': 'A area with the same name already exists'}
                    return response, status.HTTP_400_BAD_REQUEST
            area.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        area = Area.query.get_or_404(id)
        try:
            area.delete(area)
            response = {}
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class AreaListResource(AuthRequiredResource):
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=Area.query,
            resource_for_url='api.arealistresource',
            key_name='results',
            schema=area_schema)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = area_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        area_name = request_dict['name']
        if not Area.is_unique(id=0, name=area_name):
            response = {'error': 'A area with the same name already exists'}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            area = Area(area_name)
            area.add(area)
            query = Area.query.get(area.id)
            result = area_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST
