import datetime
import os
import shlex
import subprocess
import time

import pytest
import requests

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
            response = requests.get("http://{}:{}{}".format(
                get_docker_host(), port, endpoint), params=params)
        except requests.exceptions.ConnectionError:
            pass
        else:
            return response
        time.sleep(0.25)
    raise Exception("service didn't start in time")

def execute_cmd(cmd):
    assert subprocess.check_call(shlex.split(cmd)) == 0
