import shutil

from collections.abc import KeysView
from pathlib import Path

from tqdm import tqdm

from reloci.planner import Map, Planner
from reloci.renamer import BaseRenamer


class Worker:
    def __init__(
        self,
        inputpath: Path,
        outputpath: Path,
        move: bool,
        dryrun: bool,
        verbose: int,
        renamer: type[BaseRenamer],
    ) -> None:
        self.inputpath = inputpath
        self.outputpath = outputpath
        self.renamer_class = renamer

        self.move = move
        self.dryrun = dryrun
        self.verbose = verbose

    def do_the_thing(self) -> None:
        planner = Planner(
            self.inputpath,
            self.outputpath,
            self.renamer_class,
        )
        plan = planner.make_plan()

        if self.verbose == 1:
            planner.show_summary(plan)
        elif self.verbose > 1:
            planner.show_plan(plan)

        if self.dryrun:
            return

        self.make_directories(plan.keys())
        if self.move:
            self.move_files(plan)
        else:
            self.copy_files(plan)

    def make_directories(self, directories: KeysView[Path]) -> None:
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def flatten_plan(self, plan: dict[Path, list[Map]]) -> list[Map]:
        return [mapping for mappings in plan.values() for mapping in mappings]

    def move_files(self, plan: dict[Path, list[Map]]) -> None:
        for mapping in tqdm(self.flatten_plan(plan), desc='Moving files', dynamic_ncols=True):
            shutil.move(mapping.source, mapping.destination)

    def copy_files(self, plan: dict[Path, list[Map]]) -> None:
        for mapping in tqdm(self.flatten_plan(plan), desc='Copying files', dynamic_ncols=True):
            shutil.copy2(mapping.source, mapping.destination)
