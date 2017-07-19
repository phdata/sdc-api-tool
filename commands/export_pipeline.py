""" Promote an SDC pipeline from one environment to another."""
import api
import json
from commands import build_instance_url


def main(conf, args):
    """Main script entry point."""
    # Export the source pipeline and save it to file
    src = conf.config['instances'][args.src_instance]
    src_url = api.build_api_url(build_instance_url(src))
    src_auth = tuple([conf.creds['instances'][args.src_instance]['user'], conf.creds['instances'][args.src_instance]['pass']])
    export_json = api.export_pipeline(src_url, args.src_pipeline_id, src_auth)
    with open(args.out, 'w') as outFile:
        outFile.write(json.dumps(export_json, indent=4, sort_keys=False))

