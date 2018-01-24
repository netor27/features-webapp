import pytest
from unittest import TestCase
from flask import url_for, json

from web.server import create_app
from web.db import db
from web.status import status
from web.resources import UserLoginResource
from tests.integration_tests.post_helpers import PostHelper


class AuthTests(TestCase):

    @pytest.fixture(autouse=True)
    def transact(self, request, configfile, waitForDb):
        self.app = create_app(configfile, waitForDb)
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_user_name = 'testuserusers'
        self.test_user_password = 'T3s!p4s5w0RDd12#'
        self.ph = PostHelper(self.test_client, self.test_user_name, self.test_user_password)
        db.create_all()
        yield 
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_request_without_authentication(self):
        """
        Ensure we cannot access a resource that requires authentication without an appropriate authentication header
        """
        res = self.test_client.get(
            url_for('api.featurelistresource', _external=True),
            headers= self.ph.get_accept_content_type_headers())
        self.assertTrue(res.status_code == status.HTTP_401_UNAUTHORIZED)


    def test_request_with_authentication(self):
        """
        Ensure we can access a resource that requires authentication with an appropriate authentication header
        """
        user_res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(user_res.status_code, status.HTTP_201_CREATED)
        res = self.test_client.get(
            url_for('api.featurelistresource', _external=True),
            headers=self.ph.get_authentication_headers())
        self.assertTrue(res.status_code == status.HTTP_200_OK)

    def test_login_request_with_authentication(self):
        """
        Ensure we can obtain the user's data if it's logged correctly
        """
        # create a user and assert the response
        user_res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(user_res.status_code, status.HTTP_201_CREATED)        
        user_res_data = json.loads(user_res.get_data(as_text=True))
        self.assertEqual(user_res_data['name'], self.test_user_name)

        # Get the url for the login resource and query it
        url = url_for('api.userloginresource', _external=True, name=self.test_user_name)
        res = self.test_client.get(url, headers=self.ph.get_authentication_headers())
        
        # assert that the resonse is the same as the one that we created before
        self.assertTrue(res.status_code == status.HTTP_200_OK)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertTrue(res_data['id'], user_res_data['id'])
        self.assertTrue(res_data['name'], user_res_data['name'])



    def test_login_request_with_an_incorrect_authentication(self):
        """
        Ensure we can access a resource that requires authentication with an appropriate authentication header
        """
        user_res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(user_res.status_code, status.HTTP_201_CREATED)
        res = self.test_client.get(
            url_for('api.featurelistresource', _external=True))
        self.assertTrue(res.status_code == status.HTTP_401_UNAUTHORIZED)