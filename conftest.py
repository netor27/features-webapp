import pytest

def pytest_addoption(parser):
    parser.addoption("--configfile", action="store", default="configtest",
        help="Config file name")

@pytest.fixture
def configfile(request):
    return request.config.getoption("--configfile")