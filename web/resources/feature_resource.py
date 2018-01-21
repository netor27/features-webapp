from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask_httpauth import HTTPBasicAuth

from web.helpers import PaginationHelper
from web.models import Feature, FeatureSchema, Client, Area
from web.resources import AuthRequiredResource
from web.status import status
from web.db import db


feature_schema = FeatureSchema()


class FeatureResource(AuthRequiredResource):

    def get(self, id):
        feature = Feature.query.get_or_404(id)
        print(feature)
        print(feature.id)
        result = feature_schema.dump(feature).data
        print(result)
        return result

    def patch(self, id):
        feature = Feature.query.get_or_404(id)
        feature_dict = request.get_json(force=True)
        if 'title' in feature_dict:
            feature.title = feature_dict['title']
        if 'description' in feature_dict:
            feature.description = feature_dict['description']
        if 'target_date' in feature_dict:
            feature.target_date = feature_dict['target_date']
        if 'client_priority' in feature_dict:
            feature.client_priority = feature_dict['client_priority']
        dumped_feature, dump_errors = feature_schema.dump(feature)
        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST
        validate_errors = feature_schema.validate(dumped_feature)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST
        try:
            feature.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        feature = Feature.query.get_or_404(id)
        try:
            delete = feature.delete(feature)
            response = {}
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class FeatureListResource(AuthRequiredResource):
    def get(self):
        pagination_helper = PaginationHelper(
            request,
            query=Feature.query,
            resource_for_url='api.featurelistresource',
            key_name='results',
            schema=feature_schema)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = feature_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            # check the client and the area, if we receive values that doesn't exists, create them in the db
            client_name = request_dict['client']['name']
            client = Client.query.filter_by(name=client_name).first()
            if client is None:
                client = Client(name=client_name)
                db.session.add(client)

            area_name = request_dict['area']['name']
            area = Area.query.filter_by(name=area_name).first()
            if area is None:
                area = Area(name=area_name)
                db.session.add(area)

            feature = Feature(
                title=request_dict['title'],
                description=request_dict['description'],
                target_date=request_dict['target_date'],
                client_priority=request_dict['client_priority'],
                client=client,
                area=area)
            feature.add(feature)
            query = Feature.query.get(feature.id)
            result = feature_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST
