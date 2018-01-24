import pytest

def pytest_addoption(parser):
    parser.addoption("--configfile", action="store", default="configtest", help="Config file name")
    parser.addoption("--waitForDb", action="store", default="False", help="Wait until the db is ready or start the tests right away")

@pytest.fixture
def configfile(request):
    return request.config.getoption("--configfile")

@pytest.fixture
def waitForDb(request):
    wait_for_db_string = request.config.getoption("--waitForDb")
    return  wait_for_db_string == "True" or wait_for_db_string == "true"