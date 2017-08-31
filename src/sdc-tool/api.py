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

import re
import logging

import requests
import time
# required custom header for all SDC REST requests.
X_REQ_BY = {'X-Requested-By': 'pipeline-utils'}
POLLING_SECONDS = 0.25
POLL_ITERATIONS = 100

STATUS_STOPPED = 'STOPPED'
STATUS_RUNNING = 'RUNNING'
VALIDATING = 'VALIDATING'

def start_pipeline(url, pipeline_id, auth, runtime_parameters={}):
    """Start a running pipeline. The API waits for the pipeline to be fully started.

    Args:
        url                 (str): the host url in the form 'http://host:port/'.
        pipeline_id         (str): the ID of of the exported pipeline.
        auth              (tuple): a tuple of username, and password.
        runtime_parameters (dict): the desired runtime parameters for the pipeline.

    Returns:
        dict: the response json
    """
    start_result = requests.post(url + '/' + pipeline_id + '/start',
                                 headers=X_REQ_BY, auth=auth, json=runtime_parameters)
    start_result.raise_for_status()
    logging.info('Pipeline start requested.')

    poll_pipeline_status(STATUS_RUNNING, url, pipeline_id, auth)

    logging.info("Pipeline started.")
    return start_result.json()


def poll_pipeline_status(target, url, pipeline_id, auth):
    status = ""
    current_iterations = POLL_ITERATIONS

    while status != target and current_iterations > 0:
        print(status)
        time.sleep(POLLING_SECONDS)
        status = pipeline_status(url, pipeline_id, auth)['status']

    if current_iterations == 0:
        raise 'pipeline status timed out after {} seconds. Current status \'{}\''.format(str(POLL_ITERATIONS / POLLING_SECONDS), status)


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
    status_result = requests.get(url + '/' + pipeline_id + '/status', headers=X_REQ_BY, auth=auth)
    status_result.raise_for_status()
    logging.debug('Status request: ' + url + '/status')
    logging.debug(status_result.json())
    return status_result.json()

def preview_status(url, pipeline_id, previewer_id, auth):
    """Retrieve the current status for a preview.

    Args:
        url        (str): the host url in the form 'http://host:port/'.
        pipeline_id (str): the ID of of the exported pipeline.
        previewer_id (str): the previewer id created by starting a preview or validation
        auth     (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    """
    preview_status = requests.get(url + '/' + pipeline_id + '/preview/' + previewer_id + "/status", headers=X_REQ_BY, auth=auth)
    preview_status.raise_for_status()
    logging.debug(preview_status.json())
    return preview_status.json()

def poll_validation_status(url, pipeline_id, previewer_id, auth):
    status = VALIDATING
    while status == VALIDATING:
        time.sleep(POLLING_SECONDS)
        status = preview_status(url, pipeline_id, previewer_id, auth)['status']
        logging.debug('poll_validation status: {}'.format(status))

def stop_pipeline(url, pipeline_id, auth):
    """Stop a running pipeline. The API waits for the pipeline to be 'STOPPED' before returning.

    Args:
        url         (str): the host url in the form 'http://host:port/'.
        pipeline_id (str): the ID of of the exported pipeline.
        auth      (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    """

    stop_result = requests.post(url + '/' + pipeline_id + '/stop', headers=X_REQ_BY, auth=auth)
    stop_result.raise_for_status()

    logging.info("Pipeline stop requested.")

    poll_pipeline_status(STATUS_STOPPED, url, pipeline_id, auth)

    logging.info('Pipeline stopped.')
    return stop_result.json()


def validate_pipeline(url, pipeline_id, auth):
    """Validate a pipeline and show issues.

    Args:
        url         (str): the host url in the form 'http://host:port/'.
        pipeline_id (str): the ID of of the exported pipeline.
        auth      (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    """

    validate_result = requests.get(url + '/' + pipeline_id + '/validate', headers=X_REQ_BY, auth=auth)
    validate_result.raise_for_status()
    previewer_id = validate_result.json()['previewerId']
    poll_validation_status(url, pipeline_id, previewer_id, auth)

    preview_result = requests.get(url + '/' + pipeline_id + '/preview/' + validate_result.json()['previewerId'], headers=X_REQ_BY, auth=auth)
    logging.debug('result content: {}'.format(preview_result.content))

    return preview_result.json()


def import_pipeline(url, pipeline_id, auth, json_payload, overwrite = False):
    """Import a pipeline.

    This will completely overwrite the existing pipeline.

    Args:
        url          (str): the host url in the form 'http://host:port/'.
        pipeline_id   (str): the ID of of the exported pipeline.
        auth       (tuple): a tuple of username, and password.
        json_payload (dict): the exported json payload as a dictionary.
                overwrite (bool): overwrite existing pipeline

    Returns:
        dict: the response json

    """
    parameters = { 'overwrite' : overwrite }
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
        url           (str): the host url in the form 'http://host:port/'.
        auth        (tuple): a tuple of username, and password.
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

def system_info(url, auth):
    """Retrieve SDC system information.

    Args:
        url (str): the host url.
        auth (tuple): a tuple of username, and password.

    """
    sysinfo_response = requests.get(url + '/info', headers=X_REQ_BY, auth=auth)
    sysinfo_response.raise_for_status()
    print(sysinfo_response)
    return sysinfo_response.json()

def build_pipeline_url(host_url):
    """Formats the url to include the path parts for the pipeline REST API."""
    return _base_url(host_url) + '/pipeline'

def build_system_url(host_url):
    """Formats the url to include the path parts for the system REST API."""
    return _base_url(host_url) + '/system'

def _base_url(host_url):
    return re.sub(r'/$', '', host_url) + '/rest/v1'
