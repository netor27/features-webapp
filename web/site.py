from flask import Blueprint, render_template
from web.helpers import DataSeedHelper

# Setup routes
site = Blueprint('site', __name__)

@site.route("/")
def index():
    return render_template('single_page_app.html')

@site.route("/admin/initialize_demo_data")
def admin_initialize_data():
    seed = DataSeedHelper()
    users, areas, clients, features = seed.seed_demo_site()
    return render_template('initialize_data.html', users=users, areas=areas, clients=clients, features=features)

