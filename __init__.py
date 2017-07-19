import argparse
import logging
from conf import Conf
from commands import promote_pipeline, export_pipeline, import_pipeline

logging.basicConfig(level=logging.INFO)

config = Conf()


def promote_command(args):
    promote_pipeline.main(config, args)


def export_command(args):
    export_pipeline.main(config, args)


def import_command(args):
    import_pipeline.main(config, args)


def main():
    """Main script entry point."""
    parser = argparse.ArgumentParser(description='Promote an SDC pipeline from one environment to another.')
    subparsers = parser.add_subparsers(help='Sub-command')

    # promote-pipeline arguments
    promote_parser = subparsers.add_parser('promote-pipeline', help='Promote a pipeline from one SDC to another.')
    promote_parser.add_argument('--src', required=True, dest='src_instance', metavar='source_instance_name',
                        help='The instance name of the source SDC (must match the name in conf.yml)')
    promote_parser.add_argument('--dest', required=True, dest='dest_instance', metavar='dest_instance_name',
                        help='The instance name of the destination SDC (must match the name in conf.yml)')
    promote_parser.add_argument('--src-pipeline-id', required=True, dest='src_pipeline_id',
                        metavar='source-pipeline-id',
                        help='The ID of a pipeline in the source SDC')
    promote_parser.add_argument('--dest-pipeline-id', required=False, dest='dest_pipeline_id',
                        metavar='destination-pipeline-id',
                        help='The ID of a pipeline in the destination SDC')
    promote_parser.add_argument('--start', action='store_true', dest='start_dest',
                        help='Start the destination pipeline if the import is successful.')
    promote_parser.set_defaults(func=promote_command)

    # export-pipeline arguments
    export_parser = subparsers.add_parser('export-pipeline', help='Export a pipeline to a file.')
    export_parser.add_argument('--src', required=True, dest='src_instance', metavar='source',
                        help='The instance name of the source SDC (must match the name in conf.yml)')
    export_parser.add_argument('--pipelineId', required=True, dest='src_pipeline_id',
                        metavar='sourcePipelineId', help='The ID of a pipeline in the source SDC')
    export_parser.add_argument('--out', required=True, dest='out', help='Output file path')
    export_parser.set_defaults(func=export_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()