from web.models import Area, Client, User

class DataSeedHelper():

    def create_areas(self, areas):
        for a in areas:
            if Area.is_unique(id=0, name=a):
                area = Area(a)
                area.add(area)


    def create_clients(self, clients):
        for c in clients:
            if Client.is_unique(id=0, name=c):
                client = Client(c)
                client.add(client)


    def create_users(self, users):
        for key, value in users.items():
            existing_user = User.query.filter_by(name=key).first()
            if existing_user is None:
                user = User(name=key)
                user.check_password_strength_and_hash_if_ok(value)
                user.add(user)
            