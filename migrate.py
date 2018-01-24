import sys
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from web.server import create_app
from web.db import db

app = create_app("config")
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

