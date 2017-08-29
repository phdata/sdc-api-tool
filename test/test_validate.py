from base_test_case import *

def test_validate(sdc):
    execute_cmd("../sdc-tool pipeline import --dest production --pipelineJson testpipeline.json --pipelineId previewpipe")
    execute_cmd("../sdc-tool pipeline validate --host development --pipelineId previewpipe")

