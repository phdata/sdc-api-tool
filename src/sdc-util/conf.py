#    Copyright 2017 phData Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import yaml


def _read_yaml(path):
    stream = open(path, 'r')
    conf = yaml.safe_load(stream)
    stream.close()
    return conf


def read_configuration(path='sdc-hosts.yml'):
    return _read_yaml(path)


def read_credentials(path='creds.yml'):
    return _read_yaml(path)


class Conf:
    def __init__(self):
        self.config = read_configuration()
        self.creds = read_credentials()

