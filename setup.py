#!/usr/bin/env python

from distutils.core import setup

setup(name='sdc-tool',
      version='0.9',
      description='Streamsets DataCollector API utility',
      author='phData inc',
      author_email='brian@phdata.io, tony@phdata.io',
      url='phdata.io',
      install_requires=['yaml', 'requests', 'pytest'],
      packages=['sdc-tool'],
      package_dir={'sdc-tool': 'src/sdc-tool'},
      scripts=['sdc-tool']
     )
