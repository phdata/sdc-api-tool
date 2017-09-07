sdctool
=======

A set of utilities to help with management of Streamsets pipelines.

Instalation
-----------

``pip install sdctool``

Configuration
-------------

sdc-hosts.yml
^^^^^^^^^^^^^

Create a YAML file called ``sdc-hosts.yml`` in the root of the project
and fill in with details of the instances you plan to use with these
utilities. See the ``template-sdc-hosts.yml`` for an example of the
required formatting.

``template-sdc-hosts.yml``:

::

    instances:
      production:
        protocol: https
        host: production-sdc-host
        port: 18630
      stage:
        protocol: https
        host: stage-sdc-host
        port: 18630
      development:
        protocol: http
        host: dev-sdc-host
        port: 18630

creds.yml
^^^^^^^^^

Create a YAML file called ``creds.yml`` in the root of the project and
fill in with credentials of the instances you plan to use with these
utilities. See the ``template-creds.yml`` for an example of the required
formatting.

``template-creds.yml``:

::

    instances:
      production:
        user: admin
        pass: s3cr3t
      stage:
        user: admin
        pass: s35am3
      development:
        user: admin
        pass: adm1n15trat0r

Usage
^^^^^

The script ``sdc-tool`` includes help docs with details on the script
arguments.

Promote Pipeline
^^^^^^^^^^^^^^^^

Migrate one pipeline from one SDC environment to another. SDC
administrator credentials are required to execute these commands. If a
``destPipelineId`` is not specified, a new pipeline will be created with
the same name and description as the exported pipeline. Currently,
origin offset values are not part of the exported configuration, so no
manipulation of the destination's offset is required.

.. code:: bash

    $ sdc-tool pipeline promote --src dev \
      --srcPipelineId ESImport77337a4f-74c5-45d1-91fd-7ce746f1bdfd \
      --dest stage \
      --destPipelineId ESImport48b1200f-c270-4937-a226-b3443ce850f3`

Export Pipeline
^^^^^^^^^^^^^^^

Export pipeline to ``--out`` path.

.. code:: bash

    $ sdc-tool pipeline export --src dev \
      --out sdc.json \
      --pipelineId StreamManagerConsumerV06fa7c3d3-458f-4446-9f51-398899118b73

Import Pipeline
^^^^^^^^^^^^^^^

Import pipeline from ``--pipelineJson`` path.

.. code:: bash

    $ sdc-tool pipeline import --dest production \
      --pipelineJson testpipeline.json \
      --pipelineId firstpipe

Start Pipeline
^^^^^^^^^^^^^^

.. code:: bash

    $ sdc-tool pipeline start \
      --pipelineId firstpipe \
      --host production

Stop Pipeline
^^^^^^^^^^^^^

.. code:: bash

    $ sdc-tool pipeline stop \
      --pipelineId firstpipe \
      --host production

Validate Pipeline
^^^^^^^^^^^^^^^^^

Validate pipleine and return issues.

.. code:: bash

    $ sdc-tool pipeline validate \
      --pipelineId firstpipe \
      --host production

Developing
----------

This project depends on Python and Docker Compose Installing required
libraries

.. code:: bash

    pip install -r requirements.txt
