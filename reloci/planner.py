import collections
import pathlib

from dataclasses import dataclass

from .file_info import FileInfo
from .renamer import Renamer


@dataclass
class Map:
    source: pathlib.Path
    destination: pathlib.Path


class Planner:
    def __init__(self, inputpath, outputpath):
        self.inputpath = inputpath
        self.outputpath = outputpath

    def get_files(self):
        for path in self.inputpath.rglob('*'):
            if path.is_file() and not path.is_symlink():
                yield path

    def make_plan(self):
        """Create a mapping to know which input files go where in the output"""
        plan = collections.defaultdict(list)

        renamer = Renamer()
        destinations = set()

        for path in self.get_files():
            file_info = FileInfo(path)
            output_path = self.outputpath / renamer.get_output_path(file_info)

            if output_path in destinations:
                raise Exception('Duplicate destinations!')

            destinations.add(output_path)
            plan[output_path.parent].append(
                Map(
                    source=path,
                    destination=output_path,
                )
            )

        return plan

    def show_plan(self, plan):
        for directory, mappings in plan.items():
            print(f'{directory}')
            for mapping in mappings:
                print(f' {mapping.source}\t→\t{mapping.destination}')
