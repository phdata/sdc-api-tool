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

""" Retrieve SDC system information."""
import logging
import json
from commands import build_instance_url
import api

def main(conf, args):
    """Retieve SDC system information."""
    src = conf.config['instances'][args.src]
    src_url = api.build_system_url(build_instance_url(src))
    src_auth = tuple([conf.creds['instances'][args.src]['user'],
                      conf.creds['instances'][args.src]['pass']])
    sysinfo_json = api.system_info(src_url, src_auth)
    print(json.dumps(sysinfo_json, indent=4, sort_keys=False))
