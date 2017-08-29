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

""" Promote an SDC pipeline from one environment to another."""
import api
import time
from commands import build_instance_url


def main(conf, args):
    """Main script entry point."""
    # Export the source pipeline
    src = conf.config['instances'][args.src_instance]
    src_url = api.build_pipeline_url(build_instance_url(src))
    src_auth = tuple([conf.creds['instances'][args.src_instance]['user'], conf.creds['instances'][args.src_instance]['pass']])
    export_json = api.export_pipeline(src_url, args.src_pipeline_id, src_auth)

    # Import the pipeline to the destination
    dest = conf.config['instances'][args.dest_instance]
    dest_url = api.build_pipeline_url(build_instance_url(dest))
    dest_auth = tuple([conf.creds['instances'][args.dest_instance]['user'], conf.creds['instances'][args.dest_instance]['pass']])
    dest_pipeline_id = args.dest_pipeline_id
    if dest_pipeline_id:
        api.stop_pipeline(dest_url, dest_pipeline_id, dest_auth)

    else:
        # No destination pipeline id was provided, must be a new pipeline.
        create_json = api.create_pipeline(dest_url, dest_auth, export_json)
        dest_pipeline_id = create_json['info']['pipelineId']

    api.import_pipeline(dest_url, dest_pipeline_id, dest_auth, export_json)

    # Start the imported pipeline
    if args.start_dest:
        api.start_pipeline(dest_url, dest_pipeline_id, dest_auth)

