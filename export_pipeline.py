""" Promote an SDC pipeline from one environment to another."""
#!/usr/bin/python
import argparse
import getpass
import api

def main():
    """Main script entry point."""
    parser = argparse.ArgumentParser(
        description='Promote an SDC pipeine from one environment to another.')
    parser.add_argument('--hostUrl', required=True, dest='host_url', metavar='sourceHostUrl',
                        help='The host URL of the source SDC (e.g. "http://sdc-dev.phdata.io:18360/")')
    parser.add_argument('--pipelineId', required=True, dest='src_pipeline_id',
                        metavar='sourcePipelineId',
                        help='The ID of a pipeline in the source SDC')

    parser.add_argument('--out', required=True, dest='out', help='Output file path')
    args = parser.parse_args()

    # Export the source pipeline and save it to file
    src_url = api.build_api_url(args.src_host_url)
    src_creds = getpass.getpass('Source credentials (format -> username:password): ')
    src_auth = tuple(src_creds.split(':'))
    export_json = api.export(src_url, args.src_pipeline_id, src_auth)

    with open(args.out, 'w') as outFile:
        outFile.write(export_json)

if __name__ == '__main__':
    main()
