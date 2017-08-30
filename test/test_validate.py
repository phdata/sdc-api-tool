from base_test_case import *
import json

def test_validate(sdc):
    exit_code, out, err = execute_cmd("../sdc-tool pipeline import --dest production --pipelineJson testpipeline.json --pipelineId previewpipe")
    assert exit_code == 0
    exit_code, out, err = execute_cmd("../sdc-tool pipeline validate --host development --pipelineId previewpipe")
    out_parsed = json.loads(out)
    assert out_parsed['status'] == "VALID"
