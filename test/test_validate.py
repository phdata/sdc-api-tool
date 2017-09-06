from base_test_case import *
import json
from sdctool import sdc_tool
import shlex

def test_validate(sdc, capsys):
    sdc_tool.run_with_args(
        shlex.split(
            'pipeline import --overwrite --dest production --pipelineJson testpipeline.json --pipelineId previewpipe'))
    # empty capture from pipeline import
    capsys.readouterr()
    sdc_tool.run_with_args(shlex.split('pipeline validate --host development --pipelineId previewpipe'))
    out, err = capsys.readouterr()
    out_parsed = json.loads(out)
    assert out_parsed['status'] == "VALID"


def test_invalid_pipeline(sdc, capsys):
    sdc_tool.run_with_args(
        shlex.split(
            'pipeline import --overwrite --dest production --pipelineJson testpipeline-invalid.json --pipelineId previewpipe'))
    # empty capture from pipeline import
    capsys.readouterr()

    sdc_tool.run_with_args(
        shlex.split(
            'pipeline validate --host development --pipelineId previewpipe'))
    out, err = capsys.readouterr()
    out_parsed = json.loads(out)
    assert out_parsed['status'] == "VALIDATION_ERROR"
