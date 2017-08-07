from base_test_case import *

def test_start(sdc):
    execute_cmd("../sdc-util pipeline start --host production --pipelineId firstpipe")

def test_stop(sdc):
    execute_cmd("../sdc-util pipeline stop --pipelineId firstpipe --host production")

def test_start_with_params(sdc):
    execute_cmd("../sdc-util pipeline start --host production --pipelineId firstpipe --runtimeParameters '{\"foo\": 2}'")

def test_stop_with_params(sdc):
    execute_cmd("../sdc-util pipeline stop --pipelineId firstpipe --host production")
