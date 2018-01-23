from unittest import TestCase
from flask import url_for, json

from web.server import create_app
from web.db import db
from web.status import status
from web.models import Area

from tests.integration_tests.post_helpers import PostHelper


class AreasTests(TestCase):

    def setUp(self):
        self.app = create_app('configtest')
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_user_name = 'testuserAreas'
        self.test_user_password = 'T3s!p4s5w0RDd12#'
        self.ph = PostHelper(self.test_client, self.test_user_name, self.test_user_password)
        db.create_all()
    

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_and_retrieve_area(self):
        """
        Ensure we can create a new Area and then retrieve it
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # create a new area, assert we receive a 201 http code and and assert there's only one Area in the db
        new_area_name = 'New Area Name'
        post_res = self.ph.create_area(new_area_name)
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        self.assertEqual(Area.query.count(), 1)

        # check that the returned values in the post response are correct
        post_res_data = json.loads(post_res.get_data(as_text=True))
        self.assertEqual(post_res_data['name'], new_area_name)

        # get the new area url, retrieve it and assert the correct values
        area_url = post_res_data['url']
        res = self.test_client.get(
            area_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.get_data(as_text=True))
        self.assertEqual(res_data['name'], new_area_name)


    def test_create_duplicated_area(self):
        """
        Ensure we cannot create a duplicated Area
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # create a new area and assert the respose values
        new_area_name = 'New Information'
        post_res = self.ph.create_area(new_area_name)
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        self.assertEqual(Area.query.count(), 1)
        post_res_data = json.loads(post_res.get_data(as_text=True))
        self.assertEqual(post_res_data['name'], new_area_name)

        # try to assert it again, and assert the status code is an http 400
        second_post_res = self.ph.create_area(new_area_name)
        self.assertEqual(second_post_res.status_code, status.HTTP_400_BAD_REQUEST, "The insertion of a duplicate area didn't return a 400 code")
        self.assertEqual(Area.query.count(), 1)


    def test_retrieve_areas_list(self):
        """
        Ensure we can retrieve the areas list
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # create 4 areas and assert the response
        for i in range(1, 5):
            name = 'Area {}'.format(i)            
            post_res = self.ph.create_area(name)
            self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        
        # assert we only have this 4
        self.assertEqual(Area.query.count(), 4)

        # retrieve the complete list of areas, it should return only the 2 we created
        url = url_for('api.arealistresource', _external=True)
        res = self.test_client.get(
            url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.get_data(as_text=True))
        self.assertEqual(res_data['count'], 4)


    def test_update_area(self):
        """
        Ensure we can update the name for an existing area
        """
        # create our user so we can authenticate and create the area
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # create a new area and assert the result
        area_name = 'Area 1'
        post_res_1 = self.ph.create_area(area_name)
        self.assertEqual(post_res_1.status_code, status.HTTP_201_CREATED, post_res_1.get_data(as_text=True))
        post_res_data_1 = json.loads(post_res_1.get_data(as_text=True))

        # create a patch request to update the area name
        area_url = post_res_data_1['url']
        area_name_2 = 'Area 2'
        data = {'name': area_name_2}
        patch_response = self.test_client.patch(
            area_url, 
            headers=self.ph.get_authentication_headers(),
            data=json.dumps(data))
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK, patch_response.get_data(as_text=True))

        # retrieve the updated area and validate the name is the same as the updated value
        res = self.test_client.get(
            area_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.get_data(as_text=True))
        self.assertEqual(res_data['name'], area_name_2)

  
    def test_create_delete_and_retrieve_area(self):
        """
        Ensure we can create a new Area, delete it and if we retrieve it should not be there
        """
        # create our user so we can authenticate 
        res = self.ph.create_user(self.test_user_name, self.test_user_password)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.get_data(as_text=True))

        # create a new area, assert we receive a 201 http code and and assert there's only one Area in the db
        new_area_name = 'New Area Name'
        post_res = self.ph.create_area(new_area_name)
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED, post_res.get_data(as_text=True))
        self.assertEqual(Area.query.count(), 1)

        # check that the returned values in the post response are correct
        post_res_data = json.loads(post_res.get_data(as_text=True))
        self.assertEqual(post_res_data['name'], new_area_name)

        # get the new area url and delete it
        area_url = post_res_data['url']
        patch_res = self.test_client.delete(
            area_url,
            headers=self.ph.get_authentication_headers())
        
        # retrieve it and assert the correct values
        self.assertEqual(patch_res.status_code, status.HTTP_204_NO_CONTENT, patch_res.get_data(as_text=True))

        res = self.test_client.get(
            area_url,
            headers=self.ph.get_authentication_headers())
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND, res.get_data(as_text=True))