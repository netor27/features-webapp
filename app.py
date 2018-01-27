import sys
from web.server import create_app
from web.db import db

configFile = "config"
if len(sys.argv) > 1:
    configFile = sys.argv[1]

app = create_app(configFile)

if __name__ == '__main__':   
    # Create in the db the tables that are missing
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    # start the app
    app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)