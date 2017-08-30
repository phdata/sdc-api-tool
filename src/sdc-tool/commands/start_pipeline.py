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

""" Start a pipeline. """
import api
import json
from commands import build_instance_url


def main(conf, args):
    """Main script entry point."""
    host = conf.config['instances'][args.host_instance]
    url = api.build_pipeline_url(build_instance_url(host))
    auth = tuple([conf.creds['instances'][args.host_instance]['user'], conf.creds['instances'][args.host_instance]['pass']])
    runtime_parameters = {}
    if args.runtime_parameters:
        runtime_parameters = json.loads(args.runtime_parameters)
    start_result = api.start_pipeline(url, args.pipeline_id, auth, runtime_parameters)
    print(json.dumps(start_result, indent=4, sort_keys=False))


