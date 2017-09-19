from base_test_case import *
from sdctool import sdc_tool
import shlex
import uuid


pipe_id = uuid.uuid4()

def test_validate(sdc):
    sdc_tool.run_with_args(
        shlex.split(
            'pipeline import --overwrite --dest production --pipelineJson testpipeline.json --pipelineId {}'.format(pipe_id)))
    result = sdc_tool.run_with_args(shlex.split('pipeline validate --host development --pipelineId {}'.format(pipe_id)))
    assert result['status'] == "VALID"


def test_invalid_pipeline(sdc):
    sdc_tool.run_with_args(
        shlex.split(
            'pipeline import --overwrite --dest production --pipelineJson testpipeline-invalid.json --pipelineId {}'.format(pipe_id)))

    result = sdc_tool.run_with_args(
        shlex.split(
            'pipeline validate --host development --pipelineId {}'.format(pipe_id)))

    assert result['status'] == "VALIDATION_ERROR"
