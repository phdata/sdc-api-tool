# Pipeline Utils
A set of utilities to help with management of Streamsets pipelines.

## Promote
This script is indented to migrate one pipeline from one SDC environment to another. SDC administrator
credentials are required to execute these commands. The script will prompt the user to enter both
the source and destination credentials (format = username:password).
The script includes help docs with details on the script arguments, but here is an 
example of calling it from the shell:

`python promote.py --srcHostUrl "http://localhost:18630/" --srcPipelineId ESImport77337a4f-74c5-45d1-91fd-7ce746f1bdfd --destHostUrl "http://localhost:18631/" --destPipelineId ESImport48b1200f-c270-4937-a226-b3443ce850f3`


