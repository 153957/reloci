import argparse
import pathlib

from .worker import Worker


def get_parser():
    parser = argparse.ArgumentParser(
        description='Organise photos into directories by date'
    )
    parser.add_argument(
        '--move',
        action='store_true',
        help='move files to the new locations, removing them from the source location'
    )
    parser.add_argument(
        '--dryrun',
        action='store_true',
        help='do not move or copy any files, just show the actions it would take'
    )
    parser.add_argument('inputpath', type=pathlib.Path)
    parser.add_argument('outputpath', type=pathlib.Path)
    return parser


def cli():
    parser = get_parser()
    args = parser.parse_args()

    Worker(args).do_the_thing()
