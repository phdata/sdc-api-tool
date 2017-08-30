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

""" Import an SDC pipeline from a JSON file."""
import api
import json
from commands import build_instance_url


def main(conf, args):
    """Main script entry point."""
    with open(args.pipeline_json) as pipeline_json:
        dst = conf.config['instances'][args.dst_instance]
        dst_url = api.build_pipeline_url(build_instance_url(dst))
        dst_auth = tuple([conf.creds['instances'][args.dst_instance]['user'],
                          conf.creds['instances'][args.dst_instance]['pass']])
        api.import_pipeline(dst_url, args.pipeline_id, dst_auth, json.load(pipeline_json), overwrite=args.overwrite)
