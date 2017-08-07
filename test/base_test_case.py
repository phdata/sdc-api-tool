import os
import subprocess
import sys
import time
import unittest

import requests

class DockerComposeTestCase(unittest.TestCase):
    compose_file = None
    show_docker_compose_output = False
    _docker_host = "localhost"

    def setUp(self):
        compose_file = os.path.join(
            os.path.dirname(__file__), "compose",
            "{}.yml".format(self.compose_file))
        popen_kwargs = {}
        if not self.show_docker_compose_output:
            popen_kwargs = {
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
            }
        proc = subprocess.Popen(
            ["docker-compose", "-f", compose_file, "up"], **popen_kwargs)

        def cleanup():
            proc.kill()
            subprocess.call(
                ["docker-compose", "-f", compose_file, "kill"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.call(
                ["docker-compose", "-f", compose_file, "rm", "-f"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.addCleanup(cleanup)


    def get_docker_host(self):
        if not hasattr(self, "_docker_host"):
            if "linux" in sys.platform:
                docker_host = "localhost"
            else:
                docker_host = subprocess.check_output(
                    ["docker", "ip", "dev"]).strip().decode("unicode_escape")
            self._docker_host = docker_host
        return self._docker_host

    def curl_until_success(self, port, endpoint="/", params={}):
        for i in range(10):
            try:
                response = requests.get("http://{}:{}{}".format(
                    self.get_docker_host(), port, endpoint), params=params)
            except requests.exceptions.ConnectionError:
                pass
            else:
                return response
            time.sleep(1)
        else:
            raise Exception("service didn't start in time")


class BaseTestCase(DockerComposeTestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.curl_until_success(18630)
