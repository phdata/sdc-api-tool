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

""" Export an SDC pipeline from one environment to a JSON file."""
import api
import json
from commands import build_instance_url


def main(conf, args):
    """Main script entry point."""
    # Export the source pipeline and save it to file
    src = conf.config['instances'][args.src_instance]
    src_url = api.build_pipeline_url(build_instance_url(src))
    src_auth = tuple([conf.creds['instances'][args.src_instance]['user'],
                      conf.creds['instances'][args.src_instance]['pass']])
    export_json = api.export_pipeline(src_url, args.src_pipeline_id, src_auth)
    with open(args.out, 'w') as outFile:
        outFile.write(json.dumps(export_json, indent=4, sort_keys=False))
