from base_test_case import *

def test_validate(sdc):
    execute_cmd("../sdc-tool pipeline import --dest production --pipelineJson testpipeline.json --pipelineId previewpipe")
    execute_cmd("../sdc-tool pipeline validate --host development --pipelineId previewpipe")

<<<<<<< HEAD
=======
# def test_preview_start(sdc):
#     execute_cmd("../sdc-tool pipeline preview-start --pipelineId firstpipe")
#
# def test_preview_stop(sdc):
#     execute_cmd("../sdc-tool pipeline preview-stop --pipelineId firstpipe")
>>>>>>> Validate pipeline
