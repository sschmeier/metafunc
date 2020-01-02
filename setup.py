#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open("requirements.txt") as req_file:
    requirements = [x for x in req_file.read().splitlines() if not x.startswith("#")]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

# Note: the __program__ variable is set in __init__.py.
# it determines the name of the package/final command line tool.
from metafunc import __version__, __program__, __author__, __email__, __license__, __url__

setup(
    name=__program__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    python_requires='==3.6',
    packages=[__program__],
    description="An Snakemake command line interface for metafunc.",
    long_description=readme + '\n\n' + history,
    install_requires=requirements,
    test_suite='tests',
    tests_require=test_requirements,
    keywords='metafunc',
    include_package_data=True,
    setup_requires=setup_requirements,
    url=__url__,
    zip_safe=False,
    entry_points="""
      [console_scripts]
      {program} = metafunc.command:main
      """.format(
        program=__program__
    ),
    license=__license__,
)