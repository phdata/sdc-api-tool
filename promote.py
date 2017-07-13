""" Promote an SDC pipeline from one environment to another."""
#!/usr/bin/python
import argparse
import getpass
import re
import logging

import requests

logging.basicConfig(level=logging.INFO)


# required custom header for all SDC REST requests.
X_REQ_BY = {'X-Requested-By': 'pipeline-utils'}

def export(url, pipeline_id, auth):
    """Export the config and rules for a pipeline.

    Args:
        url        (str): the host url in the form 'http://host:port/'.
        pipeline_id (str): the ID of of the exported pipeline.
        auth     (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    """
    export_result = requests.get(url + '/' + pipeline_id + '/export', headers=X_REQ_BY, auth=auth)
    if export_result.status_code == 404:
        logging.error('Pipeline not found: ' + pipeline_id)
    export_result.raise_for_status()
    return export_result.json()

def status(url, pipeline_id, auth):
    """Retrieve the current status for a pipeline.

    Args:
        url        (str): the host url in the form 'http://host:port/'.
        pipeline_id (str): the ID of of the exported pipeline.
        auth     (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    """
    statust_result = requests.get(url + '/' + pipeline_id + '/status', headers=X_REQ_BY, auth=auth)
    logging.debug('Status request: ' + url + '/status')
    return statust_result.json()

def stop(url, pipeline_id, auth):
    """Stop a running pipeline.

    Args:
        url        (str): the host url in the form 'http://host:port/'.
        pipeline_id (str): the ID of of the exported pipeline.
        auth     (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    TODO: unsure whether or not this call will wait for the pipeline to come
        to a complete stop, or if it will return immediately.
    """
    stop_result = requests.post(url + '/' + pipeline_id + '/stop', headers=X_REQ_BY, auth=auth)
    stop_result.raise_for_status()
    logging.info('Pipeline stop successful.')
    return stop_result.json()

def import_pipeline(url, pipeline_id, auth, json_payload):
    """Import a pipeline.

    This will completely overwrite the existing pipeline.

    Args:
        url          (str): the host url in the form 'http://host:port/'.
        pipeline_id   (str): the ID of of the exported pipeline.
        auth       (tuple): a tuple of username, and password.
        json_payload (dict): the exported json payload as a dictionary.

    Returns:
        dict: the response json

    """
    parameters = {'overwrite':True}
    import_result = requests.post(url + '/' + pipeline_id + '/import', params=parameters,
                                  headers=X_REQ_BY, auth=auth, json=json_payload)
    if import_result.status_code != 200:
        logging.error('Import error response: ' + import_result.text)
    import_result.raise_for_status()
    logging.info('Pipeline import successful.')
    return import_result.json()

def start(url, pipeline_id, auth):
    """Start a running pipeline.

    Args:
        url        (str): the host url in the form 'http://host:port/'.
        pipeline_id (str): the ID of of the exported pipeline.
        auth     (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    TODO:
        * unsure whether or not this call will wait for the pipeline to fully
            start, or if it will return immediately.
        * add runtime parameters to the start command
    """
    start_result = requests.post(url + '/' + pipeline_id + '/start',
                                 headers=X_REQ_BY, auth=auth, json={})
    start_result.raise_for_status()
    logging.info('Pipeline start successful.')
    return start_result.json()

def create_pipeline(url, auth, json_payload):
    """Create a new pipeline.

    Args:
        url          (str): the host url in the form 'http://host:port/'.
        auth       (tuple): a tuple of username, and password.
        json_payload (dict): the exported json paylod as a dictionary.

    Returns:
        dict: the response json

    """
    title = json_payload['pipelineConfig']['title']
    description = json_payload['pipelineConfig']['description']
    params = {'description':description, 'autoGeneratePipelineId':True}
    logging.info('No destination pipeline ID provided.  Creating a new pipeline: ' + title)
    put_result = requests.put(url + '/' + title, params=params, headers=X_REQ_BY, auth=auth)
    put_result.raise_for_status()
    create_json = put_result.json()
    logging.debug(create_json)
    logging.info('Pipeline creation successful.')
    return create_json

def build_api_url(host_url):
    """Formats the url to include the path parts for the REST API."""
    return re.sub(r'/$', '', host_url) + '/rest/v1/pipeline'

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
    src_url = build_api_url(args.src_host_url)
    src_creds = getpass.getpass('Source credentials (format -> username:password): ')
    src_auth = tuple(src_creds.split(':'))
    export_json = export(src_url, args.src_pipeline_id, src_auth)

    # Import the pipeline to the destination
    dest_url = build_api_url(args.dest_host_url)
    dest_creds = getpass.getpass('Destination credentials (format -> username:password): ')
    dest_auth = tuple(dest_creds.split(':'))
    dest_pipeline_id = args.dest_pipeline_id
    if dest_pipeline_id:
        status_json = status(dest_url, dest_pipeline_id, dest_auth)

        if status_json['status'] == 'RUNNING':
            # Stop the destination pipeline
            stop(dest_url, dest_pipeline_id, dest_auth)

    else:
        # No destination pipeline id was provided, must be a new pipeline.
        create_json = create_pipeline(dest_url, dest_auth, export_json)
        dest_pipeline_id = create_json['pipeline_id']

    import_pipeline(dest_url, dest_pipeline_id, dest_auth, export_json)

    # Start the imported pipeline
    if args.start_dest:
        start(dest_url, dest_pipeline_id, dest_auth)

if __name__ == '__main__':
    main()
