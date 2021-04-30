import shutil

from reloci.planner import Planner


class Worker:
    def __init__(self, inputpath, outputpath, move, dryrun, renamer):
        self.inputpath = inputpath
        self.outputpath = outputpath
        self.renamer = renamer

        self.move = move
        self.dryrun = dryrun

    def do_the_thing(self):
        planner = Planner(
            self.inputpath,
            self.outputpath,
            self.renamer,
        )
        plan = planner.make_plan()

        if self.dryrun:
            planner.show_plan(plan)
            return

        self.make_directories(plan.keys())
        if self.move:
            self.move_files(plan)
        else:
            self.copy_files(plan)

    def make_directories(self, directories):
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def move_files(self, plan):
        for mappings in plan.values():
            for mapping in mappings:
                shutil.move(mapping.source, mapping.destination)

    def copy_files(self, plan):
        for mappings in plan.values():
            for mapping in mappings:
                shutil.copy2(mapping.source, mapping.destination)
