#!/usr/bin/env python

from setuptools import setup



setup(name='sdctool',
      version='0.9',
      description='Streamsets DataCollector API utility',
      author='phData inc',
      author_email='brian@phdata.io, tony@phdata.io',
      url='https://github.com/phdata/sdc-api-tool',
      install_requires=['pyyaml', 'requests', 'pytest'],
      packages=['sdctool'],
      scripts=['sdc-tool'],
      download_url = 'https://github.com/phdata/sdc-api-tool/tree/feature/install/dist/sdc-tool-0.9.tar.gz',
      keywords = ['streamsets', 'api', 'pipeline', 'cli']
     )

