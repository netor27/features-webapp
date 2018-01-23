[![Python](https://img.shields.io/badge/python-3.5-blue.svg)]()
[![Requirements Status](https://requires.io/github/netor27/features-webapp/requirements.svg?branch=master)](https://requires.io/github/netor27/features-webapp/requirements/?branch=master)
[![Build Status](https://travis-ci.org/netor27/features-webapp.svg?branch=master)](https://travis-ci.org/netor27/features-webapp)
[![Coverage](https://codecov.io/gh/netor27/features-webapp/branch/master/graph/badge.svg)](https://codecov.io/gh/netor27/features-webapp)


# features-webapp
Python/Flask demo web app. This API manage the following resources:

* features : Information about a specific feature that a client requested (title, description, priority, target date, area, etc. )

* clients: Client name and the relationsip to features

* areas: Area name and the relationsip to features


## Start the service with docker

Install [docker](https://docs.docker.com/engine/installation/) and run:

```shell
docker-compose build
docker-compose up -d
```

Initialize the postgre cointainer with the features schema
```shell
docker-compose run web python3 migrate.py db upgrade
```


Visit [http://localhost:5000](http://localhost:5000)

* To stop the containers

```shell
docker-compose down
```

## Start the standalone service

### Setup the PostgreSQL database

* Create a database in PostgreSQL, login as the default user (set "features" to your desired new db name)
```shell
sudo -u postgres createdb features
sudo -u postgres -i
```
* Run the psql client and create a new user with a role to manage the new db. (set 'apiuser' to your user, 'password' to your password and 'features' to your database name)

```shell
psql

CREATE ROLE apiuser WITH LOGIN PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE features TO apiuser; 
ALTER USER apiuser CREATEDB;
```

## Setting up the database schema

* Update the contents of config.py with the values for your database name, database user, database host. The current values are used for docker images

* Initialize the db via migration from flask

```shell
python migrate.py db upgrade
```

* Only if there are changes in the models that are not present on the migrations scripts, the following command must be executed to update the migration scripts

```shell
python migrate.py db migrate
```


### Running the service
* Install the requirements and run the app

```shell
pip install -r requirements.txt
python app.py
```
Visit [http://localhost:5000](http://localhost:5000)

## Development

* Create a branch for features or fixes.
* After making changes rebuild the docker images and run the containers.

```shell
docker-compose build
docker-compose up -d
```

## Tests

### Running tests inside a docker container

* Build the test images and run the tests

```shell
docker-compose -f docker-compose.tests.yml -p ci build
docker-compose -f docker-compose.tests.yml -p ci run test python -m pytest --cov=web/ tests
```

### Running tests with the standalone service

* First you need to setup a local database and update the config file with the values for your db name, user name, password and db hostname

#### Setting up the test database

* Create a database in PostgreSQL, login as the default user (set 'test_mesages' to your desired new db name)

```shell
sudo -u postgres createdb 'test_features'
sudo -u postgres -i
```

* Run the psql client and set the privileges to our previously created user to manage the new db. 

```shell
psql

GRANT ALL PRIVILEGES ON DATABASE test_features TO apiuser;
```

### Running unit tests

```shell
pip install pytest pytest-cov pytest-flask
pytest --cov=web/ tests
```
