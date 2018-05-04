[![Python](https://img.shields.io/badge/python-3.5-blue.svg)]()
[![Requirements Status](https://requires.io/github/netor27/features-webapp/requirements.svg?branch=master)](https://requires.io/github/netor27/features-webapp/requirements/?branch=master)
[![Build Status](https://travis-ci.org/netor27/features-webapp.svg?branch=master)](https://travis-ci.org/netor27/features-webapp)
[![Coverage](https://codecov.io/gh/netor27/features-webapp/branch/master/graph/badge.svg)](https://codecov.io/gh/netor27/features-webapp)


# features-webapp
This a demo app based on [this requirements](https://github.com/IntuitiveWebSolutions/EngineeringMidLevel) built with Python, Flask and KnockoutJs.
This demo consists in a Knockout.js single page application and a Python Restful API.


This app can be started using docker or running the stand-alone service.

# Getting the project

* Clone the repository in any directory you want with:
```shell
git clone git@github.com:netor27/features-webapp.git
```

* Change directory with:
```shell
cd features-webapp/
```

# Start the service with docker-compose (Recommended)

* Install [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/).

* Execute the following commands:

```shell
sudo docker-compose build
sudo docker-compose up -d
```

This will initialize the containers (one with a postgreSQL database and another with the flask app).

* For demo purposes, you can seed the app with demo data. Just open [http://localhost:80/admin/initialize_demo_data](http://localhost:80/admin/initialize_demo_data) to seed the database (Take note on one of the user/password combinations that were printed out).

That's it!, you can now login to the site with the previous credentials here [http://localhost:80](http://localhost:80).

Also, the API docs are located in here [http://localhost:80/apidocs/](http://localhost:80/apidocs/).

* To stop the containers:

```shell
sudo docker-compose down
```

## Running the tests inside a docker container

* Execute the following commands to build the test images and run the tests.

```shell
sudo docker-compose -f docker-compose.tests.yml -p ci build
sudo docker-compose -f docker-compose.tests.yml -p ci run web-tests python -m pytest --cov=web/ tests --configfile=configtestdocker
```

* That will print out the tests results and a code coverage report.
* To stop the test images, run the following command.

```shell
sudo docker-compose down
```

# Start the standalone service

## Setup a PostgreSQL database

* Create a database in PostgreSQL, login as the default user (set "features" to your desired new db name).
```shell
sudo -u postgres createdb features
sudo -u postgres -i
```
* Run the psql client and create a new user with a role to manage the new db. (set 'apiuser' to your user, 'password' to your password and 'features' to your database name).

```shell
psql

CREATE ROLE apiuser WITH LOGIN PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE features TO apiuser; 
ALTER USER apiuser CREATEDB;
```

* If you change any value, update the configuration in the config.py file with the values for your database name, user, password, host and port.

* The app will initialize the schema by itself the first time it runs.

### Running the service

* To install the requirements and run the app, execute the following commands:

```shell
pip install -r requirements.txt
python app.py
```

* For demo purposes, you can seed the app with demo data. Just open [http://localhost:80/admin/initialize_demo_data](http://localhost:80/admin/initialize_demo_data) to seed the database (Take note on one of the user/password combinations that were printed out).

That's it!, you can now login to the site with the previous credentials here [http://localhost:80](http://localhost:80).

Also, the API docs are located in here [http://localhost:80/apidocs/](http://localhost:80/apidocs/).

## Running tests with the standalone service

* First you need to setup a local database and update the config file with the values for your db name, user name, password and db hostname.

### Setting up the test database

* Create a database in PostgreSQL, login as the default user (set 'test_mesages' to your desired new db name).

```shell
sudo -u postgres createdb 'test_features'
sudo -u postgres -i
```

* Run the psql client and set the privileges to our previously created user to manage the new db. 

```shell
psql

GRANT ALL PRIVILEGES ON DATABASE test_features TO apiuser;
```

* Update the contents of configtest.py with the values for your database name, database user, database host. 

### Running tests

```shell
pip install pytest pytest-cov pytest-flask
pytest --cov=web/ tests
```

* That will print out the tests results and a code coverage report.
