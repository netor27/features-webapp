from flask import Blueprint, render_template
from web.helpers import DataSeedHelper

# Setup routes
site = Blueprint('site', __name__)

@site.route("/")
def index():
    html = "<h1>Hello world!</h1> <h3>The features api is running...</h3>"
    return html

seed_users = { "user": "Pa$$word55!", "user2": "Password1!" }
seed_areas = ['Policies', 'Billing', 'Claims', 'Reports']
seed_clients = ['Client A', 'Client B', 'Client C' ]

@site.route("/admin/initialize_data")
def admin_initialize_data():
    data_seed = DataSeedHelper()
    data_seed.create_users(seed_users)
    data_seed.create_areas(seed_areas)
    data_seed.create_clients(seed_clients)
    return render_template('initialize_data.html', users=seed_users, areas=seed_areas, clients=seed_clients)

