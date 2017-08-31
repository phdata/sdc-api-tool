from base_test_case import *
import shlex
import sdc_tool


def test_start(sdc):
    sdc_tool.main(shlex.split(
        'pipeline import --dest production --overwrite --pipelineJson testpipeline.json --pipelineId firstpipe')) # TODO put this into a setup function
    sdc_tool.main(shlex.split('pipeline start --host production --pipelineId firstpipe'))


def test_stop(sdc):
    sdc_tool.main(shlex.split('pipeline stop --pipelineId firstpipe --host production'))


def test_start_with_params(sdc):
    sdc_tool.main(shlex.split('pipeline start --host production --pipelineId firstpipe --runtimeParameters \'{\"foo\": 2}\''))


def test_stop_with_params(sdc):
    sdc_tool.main(shlex.split('pipeline stop --pipelineId firstpipe --host production'))
