from base_test_case import *
from sdctool import sdc_tool
import shlex
import uuid

pipe_id = uuid.uuid4()

def test_start(sdc):
    sdc_tool.run_with_args(shlex.split(
        'pipeline import --dest production --overwrite --pipelineJson testpipeline.json --pipelineId {}'.format(pipe_id))) # TODO put this into a setup function
    sdc_tool.run_with_args(shlex.split('pipeline start --host production --pipelineId {}'.format(pipe_id)))
    assert sdc_tool.run_with_args(
            shlex.split('pipeline status --host production --pipelineId {}'.format(pipe_id))) == 'RUNNING'


def test_stop(sdc):
    sdc_tool.run_with_args(shlex.split('pipeline stop --pipelineId {} --host production'.format(pipe_id)))
    assert sdc_tool.run_with_args(
            shlex.split('pipeline status --host production --pipelineId {}'.format(pipe_id))) == 'STOPPED'


def test_start_with_params(sdc):
    sdc_tool.run_with_args(
        shlex.split('pipeline start --host production --pipelineId {} --runtimeParameters \'{{\"foo\": 2}}\''.format(pipe_id)))
    assert sdc_tool.run_with_args(
            shlex.split('pipeline status --host production --pipelineId {}'.format(pipe_id))) == 'RUNNING'


def test_stop_with_params(sdc):
    sdc_tool.run_with_args(shlex.split('pipeline stop --pipelineId {} --host production'.format(pipe_id)))
    assert sdc_tool.run_with_args(
            shlex.split('pipeline status --host production --pipelineId {}'.format(pipe_id))) == 'STOPPED'
