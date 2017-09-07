#!/usr/bin/env python

from setuptools import setup
import pypandoc

long_description = pypandoc.convert('README.md', 'rst')

setup(name='sdctool',
      version='0.9.2',
      description='Streamsets DataCollector API utility',
      author='phData inc',
      author_email='brian@phdata.io, tony@phdata.io',
      url='https://github.com/phdata/sdc-api-tool',
      install_requires=['pyyaml', 'requests', 'pytest', 'pypandoc'],
      packages=['sdctool'],
      scripts=['sdc-tool'],
      download_url = 'https://github.com/phdata/sdc-api-tool/tree/master/dist/sdc-tool-0.9.tar.gz',
      keywords = ['streamsets', 'api', 'pipeline', 'cli'],
      long_description=long_description
     )

