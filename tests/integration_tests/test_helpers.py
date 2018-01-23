from unittest import TestCase

from web.server import create_app
from web.db import db
from web.helpers import DataSeedHelper
from web.helpers.seed_static_data import users, areas, clients, features
from web.models import Area, Client, Feature, User

# s_users = users
# s_areas = areas
# s_clients = clients
# s_features = features

class HelpersTests(TestCase):

    def setUp(self):
        self.app = create_app('configtest')
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_seed_data_create_users(self):
        # create the demo data
        seed = DataSeedHelper()
        seed.seed_demo_site()
        
        # assert the users were created correctly
        users_in_db = User.query.all()
        self.assertEqual(len(users_in_db), len(users))
        for u in users_in_db:
            self.assertTrue(u.name in users)

        # assert the areas were created correctly
        areas_in_db = Area.query.all()
        self.assertEqual(len(areas_in_db), len(areas))
        for a in areas_in_db:
            self.assertTrue(a.name in areas)

        # assert the clients were created correctly
        clients_in_db = Client.query.all()
        self.assertEqual(len(clients_in_db), len(clients))
        for c in clients_in_db:
            self.assertTrue(c.name in clients)

        # assert the features were created correctly
        self.assertEqual(Feature.query.count(), len(features))
        for f in features:
            print(f)
            db_feature = Feature.query.filter_by(title=f['title']).first()
            self.assertEqual(f['title'], db_feature.title)
            self.assertEqual(f['description'], db_feature.description)
            self.assertEqual(f['target_date'], db_feature.target_date)
            self.assertEqual(f['client_priority'], db_feature.client_priority)
            self.assertEqual(f['client'], db_feature.client.name)
            self.assertEqual(f['area'], db_feature.area.name)

