from unittest import TestCase
from flask import url_for, json
from datetime import date

from web.server import create_app
from web.db import db
from web.status import status
from web.models import Feature

from tests.integration_tests.post_helpers import PostHelper


class FeaturesTests(TestCase):

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


    def test_create_and_retrieve_feature(self):
        """
        Ensure we can create a new Feature and then retrieve it
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # create a new feature, assert we receive a 201 http code and and assert there's only one Feature in the db
        title = 'New Feature Title'
        description = "Description " * 10
        target_date = date(2018, 6, 15)
        priority = 1
        client = "Client 1"
        area = "Billing"
        post_res = self.ph.create_feature(title, description, target_date, priority, client, area)
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        self.assertEqual(Feature.query.count(), 1)

        # check that the returned values in the post response are correct
        post_res_data = json.loads(post_res.get_data(as_text=True))   
        self.assertEqual(post_res_data['title'], title)
        self.assertEqual(post_res_data['description'], description)
        self.assertEqual(post_res_data['target_date'], date)
        self.assertEqual(post_res_data['priority'], priority)
        self.assertEqual(post_res_data['client']['name'], client)
        self.assertEqual(post_res_data['area']['name'], area)

        # get the new feature url, retrieve it and assert the correct values
        feature_url = post_res_data['url']
        res = self.test_client.get(
            feature_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_data['name'], title)


    def test_retrieve_categories_list(self):
        """
        Ensure we can retrieve the categories list
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # create 2 features and assert the response
        feature_name = 'Feature 1'
        post_res_1 = self.ph.create_feature(feature_name)
        self.assertEqual(post_res_1.status_code, status.HTTP_201_CREATED)
        feature_name_2 = 'Feature 2'
        post_res_2 = self.ph.create_feature(feature_name_2)
        self.assertEqual(post_res_2.status_code, status.HTTP_201_CREATED)

        # retrieve the complete list of features, it should return only the 2 we created
        url = url_for('api.featurelistresource', _external=True)
        res = self.test_client.get(
            url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_data['count'], 2)
        self.assertEqual(res_data["results"][0]['name'], feature_name)
        self.assertEqual(res_data["results"][1]['name'], feature_name_2)


    def test_update_feature(self):
        """
        Ensure we can update the name for an existing feature
        """
        # create our user so we can authenticate and create the feature
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # create a new feature and assert the result
        feature_name = 'Feature 1'
        post_res_1 = self.ph.create_feature(feature_name)
        self.assertEqual(post_res_1.status_code, status.HTTP_201_CREATED)
        post_res_data_1 = json.loads(post_res_1.get_data(as_text=True))

        # create a patch request to update the feature name
        feature_url = post_res_data_1['url']
        feature_name_2 = 'Feature 2'
        data = {'name': feature_name_2}
        patch_response = self.test_client.patch(
            feature_url, 
            headers=self.ph.get_authentication_headers(),
            data=json.dumps(data))
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        # retrieve the updated feature and validate the name is the same as the updated value
        res = self.test_client.get(
            feature_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_data['name'], feature_name_2)

  
    def test_create_delete_and_retrieve_feature(self):
        """
        Ensure we can create a new Feature, delete it and if we retrieve it should not be there
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # create a new feature, assert we receive a 201 http code and and assert there's only one Feature in the db
        title = 'New Feature Name'
        post_res = self.ph.create_feature(title)
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feature.query.count(), 1)

        # check that the returned values in the post response are correct
        post_res_data = json.loads(post_res.get_data(as_text=True))
        self.assertEqual(post_res_data['name'], title)

        # get the new feature url and delete it
        feature_url = post_res_data['url']
        patch_res = self.test_client.delete(
            feature_url,
            headers=self.ph.get_authentication_headers())
        
        # retrieve it and assert the correct values
        self.assertEqual(patch_res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.test_client.get(
            feature_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)