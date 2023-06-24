import argparse

from importlib import import_module
from pathlib import Path

from exiftool import ExifToolHelper
from rich import print

from reloci.file_info import FileInfo
from reloci.renamer import BaseRenamer, Renamer
from reloci.worker import Worker


def get_renamer_class(import_path: str) -> type[BaseRenamer]:
    renamer_module, _, renamer_class_name = import_path.rpartition('.')
    module = import_module(renamer_module)
    renamer_class: type[BaseRenamer] = getattr(module, renamer_class_name)
    return renamer_class


def get_parser_reloci() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Organise photos into directories based on file metadata',
    )

    parser.add_argument(
        '--move',
        action='store_true',
        help='move instead of copy files to the new locations, removing them from the source location',
    )
    parser.add_argument(
        '--dryrun',
        action='store_true',
        help='do not move or copy any files, only determine the actions to take',
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='count',
        default=0,
        help='show the actions to be taken',
    )
    parser.add_argument(
        '--renamer',
        type=get_renamer_class,
        default=Renamer,
        help='provide your own BaseRenamer subclass for custom output paths',
    )

    parser.add_argument('inputpath', type=Path)
    parser.add_argument('outputpath', type=Path)

    return parser


def reloci() -> None:
    parser = get_parser_reloci()
    kwargs = vars(parser.parse_args())

    Worker(**kwargs).do_the_thing()


def get_parser_info() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Show metadata available for a given file')

    parser.add_argument('path', type=Path)

    return parser


def info() -> None:
    parser = get_parser_info()
    kwargs = vars(parser.parse_args())

    with ExifToolHelper() as exiftool:
        file_info = FileInfo(exiftool=exiftool, **kwargs)

        info = {}
        for attr in file_info.__dir__():
            if attr.startswith('_'):
                continue
            try:
                info[attr] = getattr(file_info, attr)
            except LookupError:
                info[attr] = None

        print(info)
