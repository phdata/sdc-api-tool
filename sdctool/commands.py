from . import api
import json

def build_instance_url(instance_conf):
    return instance_conf['protocol'] + '://' + instance_conf['host'] + ':' + str(instance_conf['port'])

def export_pipeline(conf, args):
    """Export a pipeline to json."""
    # Export the source pipeline and save it to file
    src = conf.config['instances'][args.src_instance]
    src_url = api.build_pipeline_url(build_instance_url(src))
    src_auth = tuple([conf.creds['instances'][args.src_instance]['user'],
                      conf.creds['instances'][args.src_instance]['pass']])
    export_json = api.export_pipeline(src_url, args.src_pipeline_id, src_auth)
    with open(args.out, 'w') as outFile:
        outFile.write(json.dumps(export_json, indent=4, sort_keys=False))

def import_pipeline(conf, args):
    """Import a pipeline from json."""
    with open(args.pipeline_json) as pipeline_json:
        dst = conf.config['instances'][args.dst_instance]
        dst_url = api.build_pipeline_url(build_instance_url(dst))
        dst_auth = tuple([conf.creds['instances'][args.dst_instance]['user'],
                          conf.creds['instances'][args.dst_instance]['pass']])
        api.import_pipeline(dst_url, args.pipeline_id, dst_auth, json.load(pipeline_json), overwrite=args.overwrite)

def promote_pipeline(conf, args):
    """Export a pipeline from a lower environment and import into higher environment."""
    src = conf.config['instances'][args.src_instance]
    src_url = api.build_pipeline_url(build_instance_url(src))
    src_auth = tuple([conf.creds['instances'][args.src_instance]['user'], conf.creds['instances'][args.src_instance]['pass']])
    export_json = api.export_pipeline(src_url, args.src_pipeline_id, src_auth)

    # Import the pipeline to the destination
    dest = conf.config['instances'][args.dest_instance]
    dest_url = api.build_pipeline_url(build_instance_url(dest))
    dest_auth = tuple([conf.creds['instances'][args.dest_instance]['user'], conf.creds['instances'][args.dest_instance]['pass']])
    dest_pipeline_id = args.dest_pipeline_id
    if dest_pipeline_id:
        api.stop_pipeline(dest_url, dest_pipeline_id, dest_auth)
    else:
        # No destination pipeline id was provided, must be a new pipeline.
        create_json = api.create_pipeline(dest_url, dest_auth, export_json)
        dest_pipeline_id = create_json['info']['pipelineId']

    api.import_pipeline(dest_url, dest_pipeline_id, dest_auth, export_json, overwrite=True)

    # Start the imported pipeline
    if args.start_dest:
        api.start_pipeline(dest_url, dest_pipeline_id, dest_auth)

def start_pipeline(conf, args):
    """Start a pipeline"""
    host = conf.config['instances'][args.host_instance]
    url = api.build_pipeline_url(build_instance_url(host))
    auth = tuple([conf.creds['instances'][args.host_instance]['user'], conf.creds['instances'][args.host_instance]['pass']])
    runtime_parameters = {}
    if args.runtime_parameters:
        runtime_parameters = json.loads(args.runtime_parameters)
    start_result = api.start_pipeline(url, args.pipeline_id, auth, runtime_parameters)
    print(json.dumps(start_result, indent=4, sort_keys=False))

def stop_pipeline(conf, args):
    """Stop a pipeline."""
    host = conf.config['instances'][args.host_instance]
    url = api.build_pipeline_url(build_instance_url(host))
    auth = tuple([conf.creds['instances'][args.host_instance]['user'], conf.creds['instances'][args.host_instance]['pass']])

    stop_result = api.stop_pipeline(url, args.pipeline_id, auth)
    print(json.dumps(stop_result, indent=4, sort_keys=False))

def system_info(conf, args):
    """Retieve SDC system information."""
    src = conf.config['instances'][args.src]
    src_url = api.build_system_url(build_instance_url(src))
    src_auth = tuple([conf.creds['instances'][args.src]['user'],
                      conf.creds['instances'][args.src]['pass']])
    sysinfo_json = api.system_info(src_url, src_auth)
    print(json.dumps(sysinfo_json, indent=4, sort_keys=False))

def validate_pipeline(conf, args):
    """Validate a pipeline configuration."""
    host = conf.config['instances'][args.host_instance]
    host_url = api.build_pipeline_url(build_instance_url(host))
    host_auth = tuple([conf.creds['instances'][args.host_instance]['user'],
                      conf.creds['instances'][args.host_instance]['pass']])
    validate_result = api.validate_pipeline(host_url, args.pipeline_id, host_auth)
    print(json.dumps(validate_result, indent=4, sort_keys=False))
