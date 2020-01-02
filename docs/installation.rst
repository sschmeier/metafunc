.. highlight:: shell

============
Installation
============

1. Install conda
----------------

On Linux::

    $ curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    $ bash Miniconda3-latest-Linux-x86_64.sh


On MacOS::

    $ curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    $ bash Miniconda3-latest-MacOSX-x86_64.sh



Add conda dir to PATH::

    $ echo 'export PATH="~/miniconda3/bin:$PATH"' >> ~/.bashrc
    $ echo 'export PATH="~/miniconda3/bin:$PATH"' >> ~/.zshrc


2. Install from source
----------------------

The sources for MetaFunc can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/sschmeier/metafunc

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/sschmeier/metafunc/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ conda create --yes -n metafunc python=3.6
    $ conda activate metafunc
    $ pip install -r requirements.txt
    $ make install


.. _Github repo: https://github.com/sschmeier/metafunc
.. _tarball: https://github.com/sschmeier/metafunc/tarball/master
