#!/usr/bin/env python

from distutils.core import setup

setup(name='sdc-utils',
      version='0.9',
      description='Streamsets DataCollector API utility',
      author='phData inc',
      author_email='brian@phdata.io, tony@phdata.io',
      url='phdata.io',
      install_requires=['yaml', 'requests', 'pytest'],
      packages=['sdc-util'],
      package_dir={'sdc-util': 'src/sdc-util'},
     )
