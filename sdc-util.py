#    Copyright 2017 phData Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import argparse
import logging
from conf import Conf
from commands import promote_pipeline, export_pipeline, import_pipeline, system_info, start_pipeline, stop_pipeline

logging.basicConfig(level=logging.INFO)

config = Conf()

def promote_command(args):
    promote_pipeline.main(config, args)

def export_command(args):
    export_pipeline.main(config, args)

def import_command(args):
    import_pipeline.main(config, args)

def info_command(args):
    system_info.main(config, args)

def start_command(args):
    start_pipeline.main(config, args)

def stop_command(args):
    stop_pipeline.main(config, args)


def define_pipeline_args(subparsers):

    pipeline_parser = subparsers.add_parser("pipeline", help='Available commands: \'import\', \'export\', \'promote\'')

    pipeline_subparsers = pipeline_parser.add_subparsers(help="Pipeline commands")

    # pipeline promote arguments
    promote_parser = pipeline_subparsers.add_parser('promote', help='Promote a pipeline from one SDC to another.')
    promote_parser.add_argument('--src', required=True, dest='src_instance', metavar='source_instance_name',
                                help='The instance name of the source SDC (must match the name in sdc-hosts.yml)')
    promote_parser.add_argument('--dest', required=True, dest='dest_instance', metavar='dest_instance_name',
                                help='The instance name of the destination SDC (must match the name in sdc-hosts.yml)')
    promote_parser.add_argument('--srcPipelineId', required=True, dest='src_pipeline_id',
                                metavar='source-pipeline-id',
                                help='The ID of a pipeline in the source SDC')
    promote_parser.add_argument('--destPipelineId', required=False, dest='dest_pipeline_id',
                                metavar='destination-pipeline-id',
                                help='The ID of a pipeline in the destination SDC')
    promote_parser.add_argument('--start', action='store_true', dest='start_dest',
                                help='Start the destination pipeline if the import is successful.')
    promote_parser.set_defaults(func=promote_command)

    # pipeline export arguments
    export_parser = pipeline_subparsers.add_parser('export', help='Export a pipeline to a file.')
    export_parser.add_argument('--src', required=True, dest='src_instance', metavar='source',
                               help='The instance name of the source SDC (must match the name in sdc-hosts.yml)')
    export_parser.add_argument('--pipelineId', required=True, dest='src_pipeline_id',
                               metavar='sourcePipelineId', help='The ID of a pipeline in the source SDC')
    export_parser.add_argument('--out', required=True, dest='out', help='Output file path')
    export_parser.set_defaults(func=export_command)

    # pipeline import arguments
    import_parser = pipeline_subparsers.add_parser('import', help='Import a pipeline from a JSON file.')
    import_parser.add_argument('--dest', required=True, dest='dst_instance', metavar='dest_instance',
                               help='The name of the destination SDC (must match an instance name in sdc-hosts.yml)')
    import_parser.add_argument('--pipelineId', required=True, dest='pipeline_id',
                               metavar='destinationPipelineId', help='The ID of a pipeline in the source SDC')
    import_parser.add_argument('--pipelineJson', required=True, dest='pipeline_json', help='Pipeline json file path')
    import_parser.set_defaults(func=import_command)

    # pipeline start arguments
    import_parser = pipeline_subparsers.add_parser('start', help='Start a pipeline.')
    import_parser.add_argument('--host', required=True, dest='host_instance', metavar='host_instance',
                               help='The name of the destination SDC (must match an instance name in sdc-hosts.yml)')
    import_parser.add_argument('--pipelineId', required=True, dest='pipeline_id',
                               metavar='destinationPipelineId', help='The ID of a pipeline in the source SDC')
    import_parser.add_argument('--runtimeParameters', required=False, dest='runtime_parameters',
                               metavar='{"HOST": "host1"}', help='JSON blob of runtime parameters')
    import_parser.set_defaults(func=start_command)

    # pipeline stop arguments
    import_parser = pipeline_subparsers.add_parser('stop', help='Stop a pipeline.')
    import_parser.add_argument('--host', required=True, dest='host_instance', metavar='host_instance',
                               help='The instance name of the target SDC (must match an instance name in sdc-hosts.yml)')
    import_parser.add_argument('--pipelineId', required=True, dest='pipeline_id',
                               metavar='destinationPipelineId', help='The ID of a pipeline in the source SDC')
    import_parser.set_defaults(func=stop_command)


def define_system_args(subparsers):
    """Append the parser arguments for the 'system' commands"""
    system_parser = subparsers.add_parser("system", help='Available commands: \'info\'')
    system_subparsers = system_parser.add_subparsers(help='System commands')

    # system info arguments
    info_parser = system_subparsers.add_parser('info', help='Get system status information')
    info_parser.add_argument('--src', required=True, dest='src', metavar='src',
                             help='The instance name of the target SDC (must match the name in sdc-hosts.yml)')
    info_parser.set_defaults(func=info_command)


def main():
    """Main script entry point."""
    parser = argparse.ArgumentParser(description='StreamSets Data Collector tools.')
    subparsers = parser.add_subparsers(help='sdc-util')

    define_pipeline_args(subparsers)
    define_system_args(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
