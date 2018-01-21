from base64 import b64encode
from flask import json, url_for


class PostHelper():

    def __init__(self, test_client, test_user_name, test_user_password):
        self.test_client = test_client
        self.test_user_name = test_user_name
        self.test_user_password = test_user_password
    
    def get_accept_content_type_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }


    def get_authentication_headers(self):
        authentication_headers = self.get_accept_content_type_headers()
        authentication_headers['Authorization'] = \
            'Basic ' + \
            b64encode((self.test_user_name + ':' + self.test_user_password).encode('utf-8')
                      ).decode('utf-8')
        return authentication_headers


    def create_user(self, name, password):
        url = url_for('api.userlistresource', _external=True)
        data = {'name': name, 'password': password}
        response = self.test_client.post(
            url,
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(data))
        return response


    def create_client(self, name):
        url = url_for('api.clientlistresource', _external=True)
        data = {'name': name}
        response = self.test_client.post(
            url,
            headers=self.get_authentication_headers(),
            data=json.dumps(data))
        return response


    def create_area(self, name):
        url = url_for('api.arealistresource', _external=True)
        data = {'name': name}
        response = self.test_client.post(
            url,
            headers=self.get_authentication_headers(),
                data=json.dumps(data))
        return response


    def create_feature(self, title, description, target_date, client_priority, client_name, area_name):
        url = url_for('api.featurelistresource', _external=True)
        data = {'title': title, 'description': description, 'target_date': target_date.strftime('%Y-%m-%dT%H:%M:%S'),
                'client_priority': client_priority, 'client': client_name, 'area': area_name}
        response = self.test_client.post(
            url,
            headers=self.get_authentication_headers(),
            data=json.dumps(data))
        return response
