# reloci

[![PyPI](https://img.shields.io/pypi/v/reloci)](https://pypi.org/project/reloci/)
[![License](https://img.shields.io/github/license/153957/reloci)](https://github.com/153957/reloci/blob/master/LICENSE)
[![Build](https://img.shields.io/github/workflow/status/153957/reloci/Run%20tests)](https://github.com/153957/reloci/actions)

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

Additionally there is a second command to view all relevant EXIF tags from a
single file, and how they are interpreted by the FileInfo class.

    $ reloci_info path/to/a/file.jpg


## Installation

If desired create a virtual environment then install this package from PyPI

    pip install reloci


## Setup for development

Create a new virtual env with Python 3.10 and install the requirements:

    conda create -n reloci python=3.10 --yes
    pip install -e .[test]
