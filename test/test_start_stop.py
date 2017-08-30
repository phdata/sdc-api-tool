from base_test_case import *

def test_start(sdc):
    exit_code, out, err = execute_cmd("../sdc-tool pipeline start --host production --pipelineId firstpipe")
    assert exit_code == 0

def test_stop(sdc):
    execute_cmd("../sdc-tool pipeline stop --pipelineId firstpipe --host production")

def test_start_with_params(sdc):
    exit_code, out, err = execute_cmd("../sdc-tool pipeline start --host production --pipelineId firstpipe --runtimeParameters '{\"foo\": 2}'")
    assert exit_code == 0

def test_stop_with_params(sdc):
    exit_code, out, err = execute_cmd("../sdc-tool pipeline stop --pipelineId firstpipe --host production")
    assert exit_code == 0
