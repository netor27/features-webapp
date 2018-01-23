from unittest import TestCase
from flask import url_for, json

from web.server import create_app
from web.db import db
from web.status import status
from web.models import User

from tests.integration_tests.post_helpers import PostHelper


class UsersTests(TestCase):

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


    def test_retrieve_users_list(self):
        """
        Ensure we can retrieve the users paginated list
        """
        # Insert our first and 6 more
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, json.loads(res.get_data(as_text=True)))

        for i in range(6):
            name, password = 'integrationTestUser{}'.format(i), 'Password1!.{}'.format(i)
            res = self.ph.create_user(name, password)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED, json.loads(res.get_data(as_text=True)))

        # Validate we have in total only 7
        self.assertEqual(User.query.count(), 7)

        # Get the first page
        first_url = url_for('api.userlistresource', _external=True)
        first_res = self.test_client.get(
            first_url,
            headers=self.ph.get_authentication_headers())
        first_res_data = json.loads(first_res.get_data(as_text=True))

        # Make sure we only get the first 5 elements
        self.assertEqual(first_res.status_code, status.HTTP_200_OK, json.loads(first_res.get_data(as_text=True)))
        self.assertEqual(first_res_data['count'], 7)
        self.assertIsNone(first_res_data['previous'])
        self.assertEqual(first_res_data['next'], url_for('api.userlistresource', page=2, size=5))
        self.assertIsNone(first_res_data['previous'])
        self.assertIsNotNone(first_res_data['results'])
        self.assertEqual(len(first_res_data['results']), 5)
        self.assertEqual(first_res_data['results'][0]['name'], self.test_user_name)

        # Get the second page, there should be only 2 elements
        second_url = url_for('api.userlistresource', page=2)
        second_res = self.test_client.get(
            second_url,
            headers=self.ph.get_authentication_headers())
        second_res_data = json.loads(second_res.get_data(as_text=True))
        self.assertEqual(second_res.status_code, status.HTTP_200_OK, json.loads(first_res.get_data(as_text=True)))
        self.assertIsNotNone(second_res_data['previous'])
        self.assertEqual(second_res_data['previous'], url_for('api.userlistresource', page=1, size=5))
        self.assertIsNone(second_res_data['next'])
        self.assertIsNotNone(second_res_data['results'])
        self.assertEqual(len(second_res_data['results']), 2)
