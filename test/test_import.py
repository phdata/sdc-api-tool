import subprocess
from .base_test_case import BaseTestCase

class TestSdcImport(BaseTestCase):
    compose_file = "sdc"

    def test_import(self):
        self.assertEquals(0, subprocess.check_call(["../sdc-util", "pipeline", "import",
                                                    "--dest", "production",
                                                    "--pipelineJson", "testpipeline.json",
                                                    "--pipelineId", "firstpipe"]))
