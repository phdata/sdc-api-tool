#!/usr/bin/env python

from setuptools import setup



setup(name='sdctool',
      version='0.9',
      description='Streamsets DataCollector API utility',
      author='phData inc',
      author_email='brian@phdata.io, tony@phdata.io',
      url='phdata.io',
      install_requires=['pyyaml', 'requests', 'pytest'],
      packages=['sdctool'],
      scripts=['sdc-tool']
     )

