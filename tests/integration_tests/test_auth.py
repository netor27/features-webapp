from unittest import TestCase
from flask import url_for, json

from web.server import create_app
from web.db import db
from web.status import status
from tests.integration_tests.post_helpers import PostHelper


class AuthTests(TestCase):

    def setUp(self):
        self.app = create_app('configtest')
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_user_name = 'testuser'
        self.test_user_password = 'T3s!p4s5w0RDd12#'
        self.ph = PostHelper(self.test_client, self.test_user_name, self.test_user_password)
        db.create_all()
    

    def tearDown(self):
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