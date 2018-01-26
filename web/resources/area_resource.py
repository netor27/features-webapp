from flask import request, jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError

from web.helpers import PaginationHelper
from web.models import Area, AreaSchema
from web.resources import AuthRequiredResource
from web.status import status
from web.db import db


area_schema = AreaSchema()

class AreaResource(AuthRequiredResource):
    def get(self, id):
        """
        Areas
        Method to retrieve a single Area
        ---
        tags:
          - Areas
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The area Id
        responses:
          200:
            description: An Area detail
            schema:
              id: Area
              properties:
                id:
                  type: int
                  description: The area Id
                  default: 0
                name:
                  type: string
                  description: The area name
                  default: "Area Name String"
                url:
                  type: string
                  description: The resource url that points to thisareauser
                  default: "http://someurl.com/api/Area/0"
        """        
        area = Area.query.get_or_404(id)
        result = area_schema.dump(area).data
        return result

    def patch(self, id):
        """
        Areas
        Method to update a single Area
        ---
        tags:
          - Areas
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The area Id
          - in: body
            name: body
            schema:
              id: AreaToUpdate
              properties:
                name:
                  type: string
                  description: The name of the Area
                  default: "Area Name String"
        responses:
          200:
            description: The updated area
            schema:
              $ref: '#/definitions/Area'              
        """
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
        """
        Areas
        Method to delete a single Area
        ---
        tags:
          - Areas
        parameters:
          - name: id
            in: path
            type: int
            required: true
            description: The area Id
        responses:
          204:
            description: No content
        """
        area = Area.query.get_or_404(id)
        try:
            area.delete(area)
            response = {"status": status.HTTP_204_NO_CONTENT}
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = {"error": str(e)}
            return resp, status.HTTP_400_BAD_REQUEST


class AreaListResource(AuthRequiredResource):
    def get(self):
        """
        Areas
        Method to query areas
        ---
        tags:
          - Areas
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
            description: An Areas list detail
            schema:
              id: AreasList
              properties:
                results:
                  type: array
                  items: 
                    $ref: '#/definitions/Area'
                previous:
                  type: string
                  description: The resource url that points to the previous page
                  default: "http://someurl.com/api/areas/?page=1&size=5"
                next:
                  type: string
                  description: The resource url that points to the next page
                  default: "http://someurl.com/api/areas/?page=3&size=5"
                count:
                  type: int
                  description: The total count of areas in the db
                  default: 10
        """ 
        pagination_helper = PaginationHelper(
            request,
            query=Area.query,
            resource_for_url='api.arealistresource',
            key_name='results',
            schema=area_schema)
        result = pagination_helper.paginate_query()
        return result

    def post(self):
        """
        Areas
        Method to create a new Area
        ---
        tags:
          - Areas
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/AreaToUpdate'
        responses:
          201:
            description: The updated area
            schema:
              $ref: '#/definitions/Area'              
        """
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
