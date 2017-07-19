""" Import an SDC pipeline from a JSON file."""
import api
import json
from commands import build_instance_url


def main(conf, args):
    """Main script entry point."""
    with open(args.pipeline_json) as pipeline_json:
        dst = conf.config['instances'][args.dst_instance]
        dst_url = api.build_api_url(build_instance_url(dst))
        dst_auth = tuple([conf.creds['instances'][args.dst_instance]['user'],
                          conf.creds['instances'][args.dst_instance]['pass']])
        api.import_pipeline(dst_url, args.pipeline_id, dst_auth, json.load(pipeline_json))
