from flask import Blueprint, render_template
from web.helpers import DataSeedHelper

# Setup routes
site = Blueprint('site', __name__)

@site.route("/")
def index():
    html = "<h1>Hello world!</h1> <h3>The features api is running...</h3>"
    return html

@site.route("/admin/initialize_demo_data")
def admin_initialize_data():
    seed = DataSeedHelper()
    users, areas, clients, features = seed.seed_demo_site()
    return render_template('initialize_data.html', users=users, areas=areas, clients=clients, features=features)

