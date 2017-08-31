import datetime
import os
import subprocess
import time
import logging
import pytest
import requests

logging.basicConfig(level=logging.INFO)

TIMEOUT_SECONDS = 30

@pytest.fixture(scope="session")
def sdc(request):
    compose_file = "compose/sdc.yml"
    popen_kwargs = {}
    proc = subprocess.Popen(["docker-compose", "-f", compose_file, "up"], **popen_kwargs)
    def cleanup():
        proc.kill()
        subprocess.call(
            ["docker-compose", "-f", compose_file, "kill"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.call(
            ["docker-compose", "-f", compose_file, "rm", "-f"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    request.addfinalizer(cleanup)
    curl_until_success(18630)
    return proc

def get_docker_host():
    docker_host = os.environ.get('DOCKER_HOST', '').strip()
    if not docker_host:
        return '127.0.0.1'
    return docker_host

def curl_until_success(port, endpoint="/", params={}):
    timeout = datetime.datetime.now() + datetime.timedelta(seconds=TIMEOUT_SECONDS)
    while datetime.datetime.now() < timeout:
        try:
            url = "http://{}:{}{}".format(
                get_docker_host(), port, endpoint)
            logging.info(url)
            response = requests.get(url, params=params)
            logging.info('polling until success status code: ' + str(response.status_code))
        except requests.exceptions.ConnectionError:
            pass
        else:
            return response
        time.sleep(0.25)
    raise Exception("service didn't start in time")
