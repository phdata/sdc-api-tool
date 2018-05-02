#!/usr/bin/env python

from setuptools import setup

version = '0.11.0'

long_description = open('README.rst').read()

setup(name='sdctool',
      version=version,
      description='Streamsets DataCollector API utility',
      author='phData inc',
      author_email='brian@phdata.io, tony@phdata.io',
      url='https://github.com/phdata/sdc-api-tool',
      install_requires=['pyyaml', 'requests', 'pytest'],
      packages=['sdctool'],
      scripts=['sdc-tool'],
      download_url='https://github.com/phdata/sdc-api-tool/tree/master/dist/sdc-tool-{}.tar.gz'.format(version),
      keywords=['streamsets', 'api', 'pipeline', 'cli'],
      long_description=long_description
      )
