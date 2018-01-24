import pytest
from unittest import TestCase
from flask import url_for, json
from datetime import date

from web.server import create_app
from web.db import db
from web.status import status
from web.models import Feature

from tests.integration_tests.post_helpers import PostHelper


class FeaturesTests(TestCase):

    @pytest.fixture(autouse=True)
    def transact(self, request, configfile):
        self.app = create_app(configfile)
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


    def test_create_and_retrieve_feature(self):
        """
        Ensure we can create a new Feature and then retrieve it
        """
        # create our user so we can authenticate
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED,
                         res.get_data(as_text=True))

        # create a new feature, assert we receive a 201 http code and and assert there's only one Feature in the db
        title = 'New Feature Title'
        description = 'Description ' * 10
        target_date = date(2018, 6, 15)
        priority = 1
        client = 'Client 1'
        area = 'Billing'
        post_res = self.ph.create_feature(
            title, description, target_date, priority, client, area)
        self.assertEqual(
            post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        self.assertEqual(Feature.query.count(), 1)

        # check that the returned values in the post response are correct
        post_res_data = json.loads(post_res.get_data(as_text=True))
        self.assertEqual(post_res_data['title'], title)
        self.assertEqual(post_res_data['description'], description)
        self.assertEqual(post_res_data['target_date'], target_date.isoformat())
        self.assertEqual(post_res_data['client_priority'], priority)
        self.assertEqual(post_res_data['client']['name'], client)
        self.assertEqual(post_res_data['area']['name'], area)

        # get the new feature url, retrieve it and assert the correct values
        feature_url = post_res_data['url']
        res = self.test_client.get(
            feature_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK,
                         res.get_data(as_text=True))
        self.assertEqual(res_data['title'], title)
        self.assertEqual(res_data['description'], description)
        self.assertEqual(res_data['target_date'], target_date.isoformat())
        self.assertEqual(res_data['client_priority'], priority)
        self.assertEqual(res_data['client']['name'], client)
        self.assertEqual(res_data['area']['name'], area)


    def test_retrieve_features_list(self):
        """
        Ensure we can retrieve the features list
        """
        # create our user so we can authenticate
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED,
                         res.get_data(as_text=True))

        # create 4 features and assert the response
        for i in range(1, 5):
            title = 'New Feature Title {}'.format(i)
            description = 'Description {}'.format(i)
            target_date = date(2018, 6, i)
            priority = i
            client = "Client"
            area = "Billing"
            post_res = self.ph.create_feature(
                title, description, target_date, priority, client, area)
            self.assertEqual(
                post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))

        # assert we only have this 4
        self.assertEqual(Feature.query.count(), 4)

        # retrieve the complete list of features, it should return only the 4 we created
        url = url_for('api.featurelistresource', _external=True)
        res = self.test_client.get(
            url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK,
                         res.get_data(as_text=True))
        self.assertEqual(res_data['count'], 4)


    def test_update_feature(self):
        """
        Ensure we can update the name for an existing feature
        """
        # create our user so we can authenticate and create the feature
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED,
                         res.get_data(as_text=True))

        # create a new feature, assert we receive a 201 http code and and assert there's only one Feature in the db
        title = 'New Feature Title'
        description = 'Description ' * 10
        target_date = date(2018, 6, 15)
        priority = 1
        client = 'Client 1'
        area = 'Billing'
        post_res = self.ph.create_feature(
            title, description, target_date, priority, client, area)
        self.assertEqual(
            post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        self.assertEqual(Feature.query.count(), 1)
        post_res_data = json.loads(post_res.get_data(as_text=True))

        # Create a new area and a new client, so we test we can update those too
        area = "New Area"
        res = self.ph.create_area(area)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))
        client = "New Client"
        res = self.ph.create_client(client)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # Create the patch request with the updated values
        feature_url = post_res_data['url']
        title = 'Updated Title'
        description = 'Updated Description ' * 10
        target_date = date(2018, 5, 19)
        priority = 15        
        data = {'title': title, 'description': description, 'target_date': target_date.isoformat(),
                'client_priority': priority, 'client': client, 'area': area}
        patch_response = self.test_client.patch(
            feature_url,
            headers=self.ph.get_authentication_headers(),
            data=json.dumps(data))
        self.assertEqual(patch_response.status_code,
                         status.HTTP_200_OK, patch_response.get_data(as_text=True))

        # retrieve the updated feature and validate the name is the same as the updated value
        res = self.test_client.get(
            feature_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.get_data(as_text=True))
        self.assertEqual(res_data['title'], title)
        self.assertEqual(res_data['description'], description)
        self.assertEqual(res_data['target_date'], target_date.isoformat())
        self.assertEqual(res_data['client_priority'], priority)
        self.assertEqual(res_data['area']['name'], area)
        self.assertEqual(res_data['client']['name'], client)


    def test_features_priority_adjustment_when_adding_a_new_feature(self):
        """
        Ensure that when creating a new feature that has the same priority as another one it should adjust the priorities

        """
        # create our user so we can authenticate
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED,
                         res.get_data(as_text=True))

        # create 4 features and assert the response
        for i in range(10):
            title = 'Title {}'.format(i+1)
            description = 'Description {}'.format(i+1)
            target_date = date(2018, 6, 1)
            priority = i+1
            client = "Client"
            area = "Billing"
            post_res = self.ph.create_feature(title, description, target_date, priority, client, area)
            self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))

        # assert we only have this 10 features (with priorities from 1 to 10)
        self.assertEqual(Feature.query.count(), 10)

        # create a new one with priority 5, so the service must update all the priorities that are higher than 5
        title = 'New Feature'
        description = 'Description'
        target_date = date(2018, 6, i)
        priority = 5
        client = "Client"
        area = "Billing"
        post_res = self.ph.create_feature(title, description, target_date, priority, client, area)
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))

        # Query all the priorities and verify they are updated correctly
        url = url_for('api.featurelistresource', _external=True, page=1, size=11)
        res = self.test_client.get(
            url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK,
                         res.get_data(as_text=True))
        self.assertEqual(res_data['count'], 11)

        # because it's a new db for this test, the id should be the same as the priority before we updated them
        features = res_data['results']
        for i in range(11):
            id = features[i]['id']
            priority = features[i]['client_priority']
            if id <= 4:
                self.assertEqual(priority, id)
            elif id == 11:
                self.assertEqual(priority, 5)
            else:
                self.assertEqual(priority, id + 1)


    def test_features_priority_adjustment_when_updating_an_existing_feature(self):
        """
        Ensure that when updating a feature that has the same priority as another one it should adjust the priorities

        """
        # create our user so we can authenticate
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED,
                         res.get_data(as_text=True))

        # create the first feature, that we will update later
        title = 'Title 1'
        description = 'Description 1'
        target_date = date(2018, 6, 1)
        priority = 1
        client = "Client"
        area = "Billing"
        post_res = self.ph.create_feature(title, description, target_date, priority, client, area)
        res_data = json.loads(post_res.get_data(as_text=True))
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        feature_url = res_data['url']

        # create other 9 features and assert the response
        for i in range(1,10):
            title = 'Title {}'.format(i+1)
            description = 'Description {}'.format(i+1)
            target_date = date(2018, 6, 1)
            priority = i+1
            client = "Client"
            area = "Billing"
            post_res = self.ph.create_feature(title, description, target_date, priority, client, area)
            res_data = json.loads(post_res.get_data(as_text=True))
            self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))

        # assert we only have this 10 features (with priorities from 1 to 10)
        self.assertEqual(Feature.query.count(), 10)

        # update a feature with priority 1 to priority 2, so the service must update all the priorities that are higher or equal than 2
        priority = 2      
        data = {'client_priority': priority}
        patch_response = self.test_client.patch(
            feature_url,
            headers=self.ph.get_authentication_headers(),
            data=json.dumps(data))
        self.assertEqual(patch_response.status_code,
                         status.HTTP_200_OK, patch_response.get_data(as_text=True))

        # Query all the priorities and verify they are updated correctly
        url = url_for('api.featurelistresource', _external=True, page=1, size=10)
        res = self.test_client.get(
            url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK,
                         res.get_data(as_text=True))
        self.assertEqual(res_data['count'], 10)

        # because it's a new db for this test, the id should be the same as the priority before we updated them
        features = res_data['results']
        for i in range(10):
            id = features[i]['id']
            priority = features[i]['client_priority']
            self.assertEqual(priority, id+1)

        
                
