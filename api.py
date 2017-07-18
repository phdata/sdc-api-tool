import requests

import re
import logging

# required custom header for all SDC REST requests.
X_REQ_BY = {'X-Requested-By': 'pipeline-utils'}


def start_pipeline(url, pipeline_id, auth):
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

def export_pipeline(url, pipeline_id, auth):
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

def pipeline_status(url, pipeline_id, auth):
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

def stop_pipeline(url, pipeline_id, auth):
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
