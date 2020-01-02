========
MetaFunc
========


.. image:: https://img.shields.io/travis/sschmeier/metafunc.svg
        :target: https://travis-ci.org/sschmeier/metafunc

.. image:: https://readthedocs.org/projects/metafunc/badge/?version=latest
        :target: https://metafunc.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/sschmeier/metafunc/shield.svg
     :target: https://pyup.io/repos/github/sschmeier/metafunc/
     :alt: Updates



An Snakemake command line interface for metafunc.

This example bundles the Snakefile with the
command line tool, but this tool can also look
in the user's working directory for Snakefiles.

Snakemake functionality is provided through
a command line tool called `metafunc`.

Quickstart
----------

This runs through the installation and usage
of `metafunc`.

Quick install
-------------

Start by setting up a conda environment,
and install the required packages into the
environment:

.. code-block:: console
    
    $ conda create --yes -n metafunc python=3.6
    $ conda activate metafunc
    $ pip install -r requirements.txt
    $ make install


Now you can run

.. code-block:: console

    $ which metafunc


and you should see `metafunc` in your
environment's `bin/` directory.


Running metafunc
----------------


.. code-block:: console

    metafunc setup -n example
    cd example
    # Edit the config.yaml to your specific project needs
    metafunc run config.yaml


Details
-------

The entrypoint of the command line interface is
the `main()` function of `metafunc/command.py`.

The location of the Snakefile is `metafunc/Snakefile`.
