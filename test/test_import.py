from base_test_case import *

def test_import(sdc):
    exit_code, out, err = execute_cmd("../sdc-tool pipeline import --dest production --overwrite --pipelineJson testpipeline.json --pipelineId firstpipe")
    assert exit_code == 0

def test_export(sdc):
    exit_code, out, err = execute_cmd("../sdc-tool pipeline export --src production --out test-results/pipeline-out.json --pipelineId firstpipe")
    assert exit_code == 0

def test_promote(sdc):
    exit_code, out, err = execute_cmd("../sdc-tool pipeline promote --src production --srcPipelineId firstpipe --dest production")
    assert exit_code == 0
