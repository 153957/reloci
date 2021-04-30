import collections
import pathlib

from dataclasses import dataclass
from functools import partial
from multiprocessing import Pool

from reloci.file_info import FileInfo


@dataclass
class Map:
    source: pathlib.Path
    destination: pathlib.Path


def get_output_path(input_path, output_root, renamer):
    file_info = FileInfo(input_path)
    return input_path, output_root / renamer.get_output_path(file_info)


class Planner:
    def __init__(self, inputpath, outputpath, renamer):
        self.input_root = inputpath
        self.output_root = outputpath
        self.renamer = renamer()

    def get_files(self):
        for path in self.input_root.rglob('*'):
            if path.is_file() and not path.is_symlink():
                yield path

    def make_plan(self):
        """Create a mapping to know which input files go where in the output"""
        plan = collections.defaultdict(list)

        destinations = set()

        input_paths = self.get_files()

        output_path_getter = partial(
            get_output_path,
            output_root=self.output_root,
            renamer=self.renamer,
        )

        with Pool() as pool:
            for input_path, output_path in pool.imap_unordered(output_path_getter, input_paths):
                if output_path in destinations:
                    raise Exception(f'Multiple files have the same destination! {output_path}')

                destinations.add(output_path)
                plan[output_path.parent].append(
                    Map(
                        source=input_path,
                        destination=output_path,
                    )
                )

        return plan

    def show_plan(self, plan):
        for directory, mappings in plan.items():
            print(f'{directory}')
            for mapping in mappings:
                print(f' {mapping.source}\t→\t{mapping.destination}')
