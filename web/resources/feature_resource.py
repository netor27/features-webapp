from datetime import datetime
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from web.helpers import PaginationHelper
from web.models import Feature, FeatureSchema, Client, Area
from web.resources import AuthRequiredResource
from web.status import status
from web.db import db


feature_schema = FeatureSchema()


class FeatureResource(AuthRequiredResource):

    def get(self, id):
        """
        Features
        Method to retrieve a single Feature
        ---
        tags:
          - Features
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The feature Id
        responses:
          200:
            description: A Feature detail
            schema:
              id: Feature
              properties:
                id:
                  type: int
                  description: The feature Id
                  default: 0
                title:
                  type: string
                  description: The title of the Feature
                  default: "Feature Name String"
                url:
                  type: string
                  description: The resource url that points to this feature
                  default: "http://someurl.com/api/features/0"
                description:
                  type: string
                  description: The description of the Feature
                  default: "Long Description string"
                target_date:
                  type: date
                  description: The target date of this feature
                  default: "2018-06-15"
                client_priority:
                  type: int
                  description: The priority a client established for this feature
                  default: 0
                creation_date:
                  type: dateTime
                  description: The date and time when this feature was created in the db
                  default: "2018-01-22T14:34:11.770289+00:00"
                area:
                  type: object
                  schema:
                    $ref: '#/definitions/Area'
                client:
                  type: object
                  schema:
                    $ref: '#/definitions/Client'
        """ 
        feature = Feature.query.get_or_404(id)
        result = feature_schema.dump(feature).data
        return result

    def patch(self, id):
        """
        Features
        Method to update a single Feature
        ---
        tags:
          - Features
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The feature Id
          - in: body
            name: body
            schema:
              id: FeatureToUpdate
              properties:
                title:
                  type: string
                  description: The title of the Feature
                  default: "Feature Name String"
                description:
                  type: string
                  description: The description of the Feature
                  default: "Long Description string"
                target_date:
                  type: date
                  description: The target date of this feature
                  default: "2018-06-15"
                client_priority:
                  type: int
                  description: The priority a client established for this feature
                  default: 0
                area:                
                  type: string
                  description: The area name
                  default: "Area 1"
                client:
                  type: string
                  description: The client name
                  default: "Client A"
        responses:
          200:
            description: The updated feature
            schema:
              $ref: '#/definitions/Feature'              
        """
        feature = Feature.query.get_or_404(id)
        feature_dict = request.get_json(force=True)
        if 'title' in feature_dict:
            feature.title = feature_dict['title']
        if 'description' in feature_dict:
            feature.description = feature_dict['description']
        if 'target_date' in feature_dict:
            feature.target_date = datetime.strptime(feature_dict['target_date'], "%Y-%m-%d")
        if 'client_priority' in feature_dict:
            feature.client_priority = int(feature_dict['client_priority'])
        if 'client' in feature_dict:
            client_name = feature_dict['client']
            client = Client.query.filter_by(name=client_name).first()
            if client is None:
                response = {'message': "The client {} doesn't exists".format(client_name)}
                return response, status.HTTP_400_BAD_REQUEST
            feature.client = client
        if 'area' in feature_dict:
            area_name = feature_dict['area']
            area = Area.query.filter_by(name=area_name).first()
            if area is None:
                response = {'message': "The area {} doesn't exists".format(area_name)}
                return response, status.HTTP_400_BAD_REQUEST
            feature.area = area

        dumped_feature, dump_errors = feature_schema.dump(feature)
        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST
        validate_errors = feature_schema.validate(dumped_feature)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST
        try:
            # only if the client priority was updated, check that we don't have the same priority as another feature, and update accordingly
            if 'client_priority' in feature_dict:
                # check that no features of the same client have the same priority, when we update the feature, the session will commit
                other_features = Feature.query.filter_by(client_id=feature.client_id).all()
                feature.adjust_features_priority(other_features)            
            feature.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        """
        Features
        Method to delete a single Feature
        ---
        tags:
          - Features
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The feature Id
        responses:
          204:
            description: No content
        """
        feature = Feature.query.get_or_404(id)
        try:
            delete = feature.delete(feature)
            response = {"status": status.HTTP_204_NO_CONTENT}
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_400_BAD_REQUEST


class FeatureListResource(AuthRequiredResource):
    def get(self):
        """
        Features
        Method to query features
        ---
        tags:
          - Features
        parameters:
          - name: page
            in: path
            type: int
            required: false
            description: The page to query
          - name: size
            in: path
            type: int
            required: false
            description: The page size
        responses:
          200:
            description: A Features list detail
            schema:
              id: FeaturesList
              properties:
                results:
                  type: array
                  items: 
                    $ref: '#/definitions/Feature'
                previous:
                  type: string
                  description: The resource url that points to the previous page
                  default: "http://someurl.com/api/features/?page=1&size=5"
                next:
                  type: string
                  description: The resource url that points to the next page
                  default: "http://someurl.com/api/features/?page=3&size=5"
                count:
                  type: int
                  description: The total count of features in the db
                  default: 10
        """ 
        pagination_helper = PaginationHelper(
            request,
            query=Feature.query,
            resource_for_url='api.featurelistresource',
            key_name='results',
            schema=feature_schema,
            order_by=Feature.client_priority)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        """
        Features
        Method to create a new Feature
        ---
        tags:
          - Features
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/FeatureToUpdate'
        responses:
          201:
            description: The updated feature
            schema:
              $ref: '#/definitions/Feature'              
        """
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

            # check that no features of the same client have the same priority, when we add the new feature, the session will commit
            other_features = Feature.query.filter_by(client_id=client.id).all()
            feature.adjust_features_priority(other_features)
            feature.add(feature)

            # query this feature from the database
            query = Feature.query.get(feature.id)
            result = feature_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST

class FeatureListByAreaResource(AuthRequiredResource):
    def get(self, id):
        """
        Features
        Method to query features from a specific Area
        ---
        tags:
          - Features
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The area Id
          - name: page
            in: path
            type: int
            required: false
            description: The page to query
          - name: size
            in: path
            type: int
            required: false
            description: The page size
        responses:
          200:
            description: A Features list detail
            schema:
              $ref: '#/definitions/FeaturesList'
        """ 
        pagination_helper = PaginationHelper(
            request,
            query=Feature.query.filter_by(area_id=id),
            resource_for_url='api.featurelistbyarearesource',
            key_name='results',
            schema=feature_schema,
            order_by=Feature.client_priority,
            paginate_id=id)
        result = pagination_helper.paginate_query()
        return result

class FeatureListByClientResource(AuthRequiredResource):
    def get(self, id):
        """
        Features
        Method to query features from a specific Client
        ---
        tags:
          - Features
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The client Id
          - name: page
            in: path
            type: int
            required: false
            description: The page to query
          - name: size
            in: path
            type: int
            required: false
            description: The page size
        responses:
          200:
            description: A Features list detail
            schema:
              $ref: '#/definitions/FeaturesList'
        """ 
        pagination_helper = PaginationHelper(
            request,
            query=Feature.query.filter_by(client_id=id),
            resource_for_url='api.featurelistbyclientresource',
            key_name='results',
            schema=feature_schema,
            order_by=Feature.client_priority,
            paginate_id=id)
        result = pagination_helper.paginate_query()
        return result