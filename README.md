# reloci

This can be used to reorganise photos into directories by date.


## Usage

This is a command line utility to copy or move files from one location
to another location using the metadata in the files to order them
into logical directories.

    $ reloci current/path/to/files path/to/destination

To see all options use

    $ reloci --help

Currently the files will be ordered based on the creation date of the
files. Use the `dryrun` option to check if the planned move/copy matches
your expectations.


## Installation

If desired create a virtual environment then install this package from PyPI

    pip install reloci


## Setup for development

Create a new virtual env with Python 3.9 and install the requirements:

    conda create -n reloci python=3.9 --yes
    pip install -e .[test]
