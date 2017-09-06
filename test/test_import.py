from base_test_case import *
from sdctool import sdc_tool
import shlex


def test_import(sdc, capsys):
    sdc_tool.run_with_args(shlex.split('pipeline import --dest production --overwrite --pipelineJson testpipeline.json --pipelineId firstpipe'))


def test_export(sdc):
    sdc_tool.run_with_args(shlex.split('pipeline export --src production --out test-results/pipeline-out.json --pipelineId firstpipe'))


def test_promote(sdc):
    sdc_tool.run_with_args(shlex.split('pipeline promote --src production --srcPipelineId firstpipe --dest production'))
