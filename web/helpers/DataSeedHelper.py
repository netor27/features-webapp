from web.models import Area, Client, User, Feature
from web.helpers.seed_static_data import users, areas, clients, features

"""
"""
class DataSeedHelper():

    def seed_demo_site(self):
        self.create_users()
        self.create_areas()
        self.create_clients()
        self.create_features()
        return users, areas, clients, features


    def create_areas(self):
        for a in areas:
            if Area.is_unique(id=0, name=a):
                area = Area(a)
                area.add(area)


    def create_clients(self):
        for c in clients:
            if Client.is_unique(id=0, name=c):
                client = Client(c) 
                client.add(client)


    def create_users(self):
        for key, value in users.items():
            existing_user = User.query.filter_by(name=key).first()
            if existing_user is None:
                user = User(name=key)
                user.check_password_strength_and_hash_if_ok(value)
                user.add(user)
            

    def create_features(self):        
        for f in features:
            title = f['title']
            existing = Feature.query.filter_by(title=title).first()
            if existing is None:
                client_name = f['client']
                client = Client.query.filter_by(name=client_name).first()            
                area_name = f['area']
                area = Area.query.filter_by(name=area_name).first()               
                feature = Feature(
                    title=title,
                    description=f['description'],
                    target_date=f['target_date'],
                    client_priority=f['client_priority'],
                    client=client,
                    area=area)
                feature.add(feature)

