import collections
import pathlib

from dataclasses import dataclass

from exiftool import ExifToolHelper
from tqdm import tqdm

from reloci.file_info import FileInfo


@dataclass
class Map:
    source: pathlib.Path
    destination: pathlib.Path


class Planner:
    def __init__(self, inputpath, outputpath, renamer):
        self.input_root = inputpath
        self.output_root = outputpath
        self.renamer = renamer()

    def get_files(self):
        return [
            path
            for path in self.input_root.rglob('*')
            if path.is_file() and not path.is_symlink() and not path.name.startswith('.')
        ]

    def get_output_path(self, input_path, exiftool):
        try:
            file_info = FileInfo(input_path, exiftool)
            return self.output_root / self.renamer.get_output_path(file_info)
        except LookupError:
            return self.get_output_path_from_counterpart(input_path, exiftool)

    def get_output_path_from_counterpart(self, input_path, exiftool):
        try:
            counterpart_path = next(
                path
                for path in input_path.parent.rglob(f'{input_path.stem}.*')
                if path != input_path
            )
        except StopIteration:
            raise LookupError('Unable to find a counterpart file')

        file_info = FileInfo(counterpart_path, exiftool)
        file_path = self.renamer.get_output_path(file_info)
        return self.output_root / file_path.parent / (file_path.stem + input_path.suffix)

    def make_plan(self):
        """Create a mapping to know which input files go where in the output"""
        plan = collections.defaultdict(list)

        destinations = set()

        input_paths = self.get_files()

        with ExifToolHelper() as exiftool:
            for input_path in tqdm(input_paths, desc='Reading input', dynamic_ncols=True):
                output_path = self.get_output_path(input_path, exiftool)

                if output_path in destinations:
                    raise Exception(f'Multiple files have the same destination!\n {input_path}\t???\t{output_path}.')

                if output_path.is_file():
                    raise Exception(f'A file already exists at destination path!\n {input_path}\t???\t{output_path}.')

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
                print(f' {mapping.source}\t???\t{mapping.destination}')
