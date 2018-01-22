from unittest import TestCase
from flask import url_for, json

from web.server import create_app
from web.db import db
from web.status import status
from web.models import Client

from tests.integration_tests.post_helpers import PostHelper


class ClientsTests(TestCase):

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


    def test_create_and_retrieve_client(self):
        """
        Ensure we can create a new Client and then retrieve it
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # create a new client, assert we receive a 201 http code and and assert there's only one Client in the db
        new_client_name = 'New Client Name'
        post_res = self.ph.create_client(new_client_name)
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        self.assertEqual(Client.query.count(), 1)

        # check that the returned values in the post response are correct
        post_res_data = json.loads(post_res.get_data(as_text=True))
        self.assertEqual(post_res_data['name'], new_client_name)

        # get the new client url, retrieve it and assert the correct values
        client_url = post_res_data['url']
        res = self.test_client.get(
            client_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.get_data(as_text=True))
        self.assertEqual(res_data['name'], new_client_name)


    def test_create_duplicated_client(self):
        """
        Ensure we cannot create a duplicated Client
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # create a new client and assert the respose values
        new_client_name = 'New Information'
        post_res = self.ph.create_client(new_client_name)
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        self.assertEqual(Client.query.count(), 1)
        post_res_data = json.loads(post_res.get_data(as_text=True))
        self.assertEqual(post_res_data['name'], new_client_name)

        # try to assert it again, and assert the status code is an http 400
        second_post_res = self.ph.create_client(new_client_name)
        self.assertEqual(second_post_res.status_code, status.HTTP_400_BAD_REQUEST, "The insertion of a duplicate client didn't return a 400 code")
        self.assertEqual(Client.query.count(), 1)


    def test_retrieve_clients_list(self):
        """
        Ensure we can retrieve the clients list
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # create 4 clients and assert the response
        for i in range(1, 5):
            name = 'Client {}'.format(i)            
            post_res = self.ph.create_client(name)
            self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        
        # assert we only have this 4
        self.assertEqual(Client.query.count(), 4)

        # retrieve the complete list of clients, it should return only the 2 we created
        url = url_for('api.clientlistresource', _external=True)
        res = self.test_client.get(
            url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.get_data(as_text=True))
        self.assertEqual(res_data['count'], 4)


    def test_update_client(self):
        """
        Ensure we can update the name for an existing client
        """
        # create our user so we can authenticate and create the client
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # create a new client and assert the result
        client_name = 'Client 1'
        post_res_1 = self.ph.create_client(client_name)
        self.assertEqual(post_res_1.status_code, status.HTTP_201_CREATED, post_res_1.get_data(as_text=True))
        post_res_data_1 = json.loads(post_res_1.get_data(as_text=True))

        # create a patch request to update the client name
        client_url = post_res_data_1['url']
        client_name_2 = 'Client 2'
        data = {'name': client_name_2}
        patch_response = self.test_client.patch(
            client_url, 
            headers=self.ph.get_authentication_headers(),
            data=json.dumps(data))
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK, patch_response.get_data(as_text=True))

        # retrieve the updated client and validate the name is the same as the updated value
        res = self.test_client.get(
            client_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.get_data(as_text=True))
        self.assertEqual(res_data['name'], client_name_2)

  
    def test_create_delete_and_retrieve_client(self):
        """
        Ensure we can create a new Client, delete it and if we retrieve it should not be there
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # create a new client, assert we receive a 201 http code and and assert there's only one Client in the db
        new_client_name = 'New Client Name'
        post_res = self.ph.create_client(new_client_name)
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        self.assertEqual(Client.query.count(), 1)

        # check that the returned values in the post response are correct
        post_res_data = json.loads(post_res.get_data(as_text=True))
        self.assertEqual(post_res_data['name'], new_client_name)

        # get the new client url and delete it
        client_url = post_res_data['url']
        patch_res = self.test_client.delete(
            client_url,
            headers=self.ph.get_authentication_headers())
        
        # retrieve it and assert the correct values
        self.assertEqual(patch_res.status_code, status.HTTP_204_NO_CONTENT, patch_res.get_data(as_text=True))

        res = self.test_client.get(
            client_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND, res.get_data(as_text=True))