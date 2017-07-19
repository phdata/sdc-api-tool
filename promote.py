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
#!/usr/bin/python
import argparse
import getpass
import api
import logging
import time


def main():
    """Main script entry point."""
    parser = argparse.ArgumentParser(
        description='Promote an SDC pipeine from one environment to another.')
    parser.add_argument('--srcHostUrl', required=True, dest='src_host_url', metavar='sourceHostUrl',
                        help='The host URL of the source SDC (e.g. "http://sdc-dev.phdata.io:18360/")')
    parser.add_argument('--srcPipelineId', required=True, dest='src_pipeline_id',
                        metavar='sourcePipelineId',
                        help='The ID of a pipeline in the source SDC')
    parser.add_argument('--destHostUrl', required=True, dest='dest_host_url',
                        metavar='destinationHostUrl',
                        help='The host URL of the destination SDC (e.g. "http://sdc-prod.phdata.io:18360/")')
    parser.add_argument('--destPipelineId', required=False, dest='dest_pipeline_id',
                        metavar='destintionPipelineId',
                        help='The ID of a pipeline in the destination SDC')
    parser.add_argument('--start', action='store_true', dest='start_dest',
                        help='Start the destination pipeline if the import is successful.')
    args = parser.parse_args()

    # Export the source pipeline
    src_url = api.build_api_url(args.src_host_url)
    src_creds = getpass.getpass('Source credentials (format -> username:password): ')
    src_auth = tuple(src_creds.split(':'))
    export_json = api.export_pipeline(src_url, args.src_pipeline_id, src_auth)

    # Import the pipeline to the destination
    dest_url = api.build_api_url(args.dest_host_url)
    dest_creds = getpass.getpass('Destination credentials (format -> username:password): ')
    dest_auth = tuple(dest_creds.split(':'))
    dest_pipeline_id = args.dest_pipeline_id
    if dest_pipeline_id:
        status_json = api.pipeline_status(dest_url, dest_pipeline_id, dest_auth)
        if status_json['status'] == 'RUNNING':
            # Stop the destination pipeline
            api.stop_pipeline(dest_url, dest_pipeline_id, dest_auth)
            while status_json['status'] != 'STOPPED':
                time.sleep(2)
                status_json = api.pipeline_status(dest_url, dest_pipeline_id, dest_auth)

    else:
        # No destination pipeline id was provided, must be a new pipeline.
        create_json = api.create_pipeline(dest_url, dest_auth, export_json)
        dest_pipeline_id = create_json['pipeline_id']

    api.import_pipeline(dest_url, dest_pipeline_id, dest_auth, export_json)

    # Start the imported pipeline
    if args.start_dest:
        api.start_pipeline(dest_url, dest_pipeline_id, dest_auth)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
