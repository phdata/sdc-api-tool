#!/usr/bin/python
import argparse
import requests
import getpass
import re
import logging
""" Promote an SDC pipeline from one environment to another."""
logging.basicConfig(level = logging.INFO)

parser = argparse.ArgumentParser(description='Promote an SDC pipeine from one environment to another.')
parser.add_argument('--srcHostUrl', required=True, dest='srcHostUrl', metavar='sourceHostUrl', help='The host URL of the source SDC (e.g. "http://sdc-dev.phdata.io:18360/")')
parser.add_argument('--srcPipelineId', required=True, dest='srcPipelineId', metavar='sourcePipelineId', help='The ID of a pipeline in the source SDC')
parser.add_argument('--destHostUrl', required=True, dest='destHostUrl', metavar='destinationHostUrl', help='The host URL of the destination SDC (e.g. "http://sdc-prod.phdata.io:18360/")')
parser.add_argument('--destPipelineId', required=False, dest='destPipelineId', metavar='destintionPipelineId', help='The ID of a pipeline in the destination SDC')
parser.add_argument('--start', action='store_true', dest='startDest', help='Start the destination pipeline if the import is successful.')
args = parser.parse_args()

# required custom header for all SDC REST requests.
xReqBy = {'X-Requested-By':'pipeline-utils'}

def export(url, pipelineId, auth):
    """Export the config and rules for a pipeline.

    Args:
        url        (str): the host url in the form 'http://host:port/'.
        pipelineId (str): the ID of of the exported pipeline.
        auth     (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    """
    exportResult = requests.get(url + '/' + pipelineId + '/export', headers=xReqBy, auth=auth)
    if exportResult.status_code == 404:
        logging.error('Pipeline not found: ' + pipelineId)
    exportResult.raise_for_status()
    return exportResult.json()

def status(url, pipelineId, auth):
    """Retrieve the current status for a pipeline.

    Args:
        url        (str): the host url in the form 'http://host:port/'.
        pipelineId (str): the ID of of the exported pipeline.
        auth     (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    """
    statustResult = requests.get(url + '/' + pipelineId + '/status', headers=xReqBy, auth=auth)
    logging.debug('Status request: ' + url + '/status')
    return statustResult.json()

def stop(url, pipelineId, auth):
    """Stop a running pipeline.

    Args:
        url        (str): the host url in the form 'http://host:port/'.
        pipelineId (str): the ID of of the exported pipeline.
        auth     (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    TODO: unsure whether or not this call will wait for the pipeline to come
        to a complete stop, or if it will return immediately.
    """
    stopResult = requests.post(url + '/' + pipelineId + '/stop', headers=xReqBy, auth=auth)
    stopResult.raise_for_status()
    logging.info('Pipeline stop successful.')
    return stopResult.json()

def importPipeline(url, pipelineId, auth, jsonPayload):
    """Import a pipeline.

    This will completely overwrite the existing pipeline.

    Args:
        url          (str): the host url in the form 'http://host:port/'.
        pipelineId   (str): the ID of of the exported pipeline.
        auth       (tuple): a tuple of username, and password.
        jsonPayload (dict): the exported json payload as a dictionary.

    Returns:
        dict: the response json

    """
    parameters = {'overwrite':True}
    importResult = requests.post(url + '/' + pipelineId + '/import', params=parameters, headers=xReqBy, auth=auth, json=jsonPayload)
    if importResult.status_code != 200:
        logging.error('Import error response: ' + importResult.text)
    importResult.raise_for_status()
    logging.info('Pipeline import successful.')
    return importResult.json()

def start(url, pipelineId, auth):
    """Start a running pipeline.

    Args:
        url        (str): the host url in the form 'http://host:port/'.
        pipelineId (str): the ID of of the exported pipeline.
        auth     (tuple): a tuple of username, and password.

    Returns:
        dict: the response json

    TODO: 
        * unsure whether or not this call will wait for the pipeline to fully
            start, or if it will return immediately.
        * add runtime parameters to the start command
    """
    startResult = requests.post(url + '/' + pipelineId + '/start', headers=xReqBy, auth=auth, json={})
    startResult.raise_for_status()
    logging.info('Pipeline start successful.')
    return startResult.json()

def createPipeline(url, auth, jsonPayload):
    """Create a new pipeline.

    Args:
        url          (str): the host url in the form 'http://host:port/'.
        auth       (tuple): a tuple of username, and password.
        jsonPayload (dict): the exported json paylod as a dictionary.

    Returns:
        dict: the response json

    """
    title, description = exportJson['pipelineConfig']['title'], exportJson['pipelineConfig']['description']
    params = {'description':description, 'autoGeneratePipelineId':True}
    logging.info('No destination pipeline ID provided.  Creating a new pipeline: ' + title)
    putResult = requests.put(url + '/' + title, params=params, headers=xReqBy, auth=auth)
    putResult.raise_for_status()
    createJson = putResult.json()
    logging.debug(createJson)
    logging.info('Pipeline creation successful.')
    return createJson

def buildAPIUrl(hostUrl):
    return re.sub(r'/$', '', hostUrl) + '/rest/v1/pipeline'

# Export the source pipeline
srcUrl = buildAPIUrl(args.srcHostUrl)
srcCreds = getpass.getpass('Source credentials (format -> username:password): ')
srcAuth = tuple(srcCreds.split(':'))
exportJson = export(srcUrl, args.srcPipelineId, srcAuth)

# Import the pipeline to the destination
destUrl = buildAPIUrl(args.destHostUrl)
destCreds = getpass.getpass('Destination credentials (format -> username:password): ')
destAuth = tuple(destCreds.split(':'))
destPipelineId = args.destPipelineId
if destPipelineId and len(destPipelineId) > 0:
    statusJson = status(destUrl, destPipelineId, destAuth)

    if statusJson['status'] == 'RUNNING':
        # Stop the destination pipeline
        stop(destUrl, destPipelineId, destAuth)

else:
    # No destination pipeline id was provided, must be a new pipeline.
    createJson = createPipeline(destUrl, destAuth, exportJson)
    destPipelineId = createJson['pipelineId']

importPipeline(destUrl, destPipelineId, destAuth, exportJson)

# Start the imported pipeline
if args.startDest:
    start(destUrl, destPipelineId, destAuth)


