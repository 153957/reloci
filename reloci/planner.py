import collections

from dataclasses import dataclass
from operator import attrgetter
from pathlib import Path

from exiftool import ExifToolHelper
from tqdm import tqdm

from reloci.file_info import FileInfo
from reloci.renamer import BaseRenamer


@dataclass
class Map:
    source: Path
    destination: Path


class Planner:
    def __init__(self, inputpath: Path, outputpath: Path, renamer: type[BaseRenamer]) -> None:
        self.input_root = inputpath
        self.output_root = outputpath
        self.renamer = renamer()

    def get_files(self) -> list[Path]:
        """Get list of all visible files (non symlinks) in input path"""
        return [
            path
            for path in self.input_root.rglob('*')
            if path.is_file() and not path.is_symlink() and not path.name.startswith('.')
        ]

    def get_output_path(self, input_path: Path, exiftool: ExifToolHelper) -> Path:
        """For a given file path determine the output path using the provided renamer

        First try to get the best (most accurate) rename option for the input file.
        If not available, try using information from counterpart files.
        If that fails, use the fallback rename option for the input file.

        """
        try:
            file_info = FileInfo(input_path, exiftool)
            return self.output_root / self.renamer.get_output_path(file_info)
        except LookupError:
            try:
                return self.get_output_path_from_counterpart(input_path, exiftool)
            except LookupError:
                if hasattr(self.renamer, 'get_fallback_output_path'):
                    return self.output_root / self.renamer.get_fallback_output_path(file_info)
                raise

    def get_output_path_from_counterpart(self, input_path: Path, exiftool: ExifToolHelper) -> Path:
        """Attempt to find an accurate rename option for a counterpart file

        Find a file with the same base filename but with a different file extension.
        Try to get an accurate rename option for this file.

        """
        try:
            counterpart_path = next(
                path
                for path in input_path.parent.rglob(f'{input_path.stem}.*')
                if path != input_path and path.suffix.casefold() != '.aae'
            )
        except StopIteration:
            raise LookupError('Unable to find a counterpart file') from None

        file_info = FileInfo(counterpart_path, exiftool)
        file_path = self.renamer.get_output_path(file_info)
        return self.output_root / file_path.parent / (file_path.stem + input_path.suffix)

    def make_plan(self) -> dict[Path, list[Map]]:
        """Create a mapping to know which input files go where in the output"""
        plan = collections.defaultdict(list)

        destinations = set()

        input_paths = self.get_files()

        with ExifToolHelper() as exiftool:
            for input_path in tqdm(input_paths, desc='Reading input', dynamic_ncols=True):
                output_path = self.get_output_path(input_path, exiftool)

                if output_path in destinations:
                    raise OSError(f'Multiple files have the same destination!\n {input_path}\t→\t{output_path}.')

                if output_path.is_file():
                    raise FileExistsError(
                        f'A file already exists at destination path!\n {input_path}\t→\t{output_path}.',
                    )

                destinations.add(output_path)

                plan[output_path.parent].append(
                    Map(
                        source=input_path,
                        destination=output_path,
                    ),
                )

        return plan

    def show_summary(self, plan: dict[Path, list[Map]]) -> None:
        for directory, mappings in sorted(plan.items()):
            print(f'{len(mappings): 5d} → {directory}')

    def show_plan(self, plan: dict[Path, list[Map]]) -> None:
        for directory, mappings in plan.items():
            print(f'{directory}')
            for mapping in sorted(mappings, key=attrgetter('destination')):
                print(f' {mapping.source}\t→\t{mapping.destination}')
