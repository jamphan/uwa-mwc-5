import pytest
import configparser
import os

from trashyApp.conf import get_config, Config

TEST_PATH = './test_config.ini'

# Base test configuration
TEST_CONF = """
[MQTT]
broker_url = m2m.eclipse.org
topics_subscribe = UWA/CITS/DATA; Test/Topic;Hello;

[DATABASE]
type = json
path = somewhere
file = data.json

[FLASK]
server_name = 0.0.0.0:6000
debug = True
"""

TEST_CONF_WITH_DEFAULTS = """
[MQTT]
broker_url = m2m.eclipse.org
topics_subscribe = UWA/CITS/DATA; Test/Topic;Hello;

[DATABASE]
type = json
path =
file = data.json

[FLASK]
server_name = 
debug = True
"""

@pytest.fixture
def testconfigraw():
    with open(TEST_PATH, 'w') as fd:
        fd.write(TEST_CONF)

    yield TEST_PATH

    os.remove(TEST_PATH)

@pytest.fixture
def testconfig():
    with open(TEST_PATH, 'w') as fd:
        fd.write(TEST_CONF)

    c = Config(path=TEST_PATH)
    yield c
    
    os.remove(TEST_PATH)

@pytest.fixture
def testconfig_withdefaults():
    with open(TEST_PATH, 'w') as fd:
        fd.write(TEST_CONF_WITH_DEFAULTS)

    c = Config(path=TEST_PATH)
    yield c
    
    os.remove(TEST_PATH)

def test_configure_basic(testconfigraw):

    c = get_config(testconfigraw)
    assert c['DATABASE']['type'] == 'json'

def test_configure_getItem(testconfigraw):

    c = get_config(testconfigraw)
    assert c['MQTT']['broker_url'] == 'm2m.eclipse.org'
    assert c['DATABASE']['path'] == 'somewhere'
    assert bool(c['FLASK']['debug'])

def test_configure_listMqttTopics(testconfigraw):

    c = get_config(testconfigraw)

    topic_list = [x.strip() for x in c['MQTT']['topics_subscribe'].split(';') if x.strip() != '']

    assert topic_list == ['UWA/CITS/DATA', 'Test/Topic', 'Hello']

def test_appconfig_basic(testconfig):

    assert testconfig.SERVER_NAME == '0.0.0.0:6000'
    assert testconfig.DATABASE_TYPE == 'json'
    assert testconfig.DATABASE_PATH == os.path.join('somewhere', 'data.json')
    assert testconfig.DEBUG
    assert testconfig.MQTT_BROKER_URL == 'm2m.eclipse.org'
    assert testconfig.MQTT_TOPICS == ['UWA/CITS/DATA', 'Test/Topic', 'Hello']

def test_appconfig_withdefaults(testconfig_withdefaults):

    assert testconfig_withdefaults.SERVER_NAME == '127.0.0.1:5000'
    assert testconfig_withdefaults.DATABASE_TYPE == 'json'
    assert testconfig_withdefaults.DATABASE_PATH == os.path.join('.', 'data.json')
    assert testconfig_withdefaults.DEBUG
    assert testconfig_withdefaults.MQTT_BROKER_URL == 'm2m.eclipse.org'
    assert testconfig_withdefaults.MQTT_TOPICS == ['UWA/CITS/DATA', 'Test/Topic', 'Hello']