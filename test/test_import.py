from base_test_case import *

def test_import(sdc):
    execute_cmd("../sdc-util pipeline import --dest production --pipelineJson testpipeline.json --pipelineId firstpipe")

def test_export(sdc):
    execute_cmd("../sdc-util pipeline export --src production --out test-results/pipeline-out.json --pipelineId firstpipe")

def test_promote(sdc):
    execute_cmd("../sdc-util pipeline promote --src production --srcPipelineId firstpipe --dest production")
