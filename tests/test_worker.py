import tempfile
import unittest

from pathlib import Path

from reloci import planner, renamer, worker


class WorkerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.worker = worker.Worker(
            inputpath=Path(),
            outputpath=Path(),
            move=True,
            dryrun=True,
            verbose=0,
            renamer=renamer.Renamer,
        )

    def test_make_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = Path(tmp_dir)
            paths = {
                base / '2020/12/201211': None,
                base / '2024/10': None,
                base / '2024': None,
                base / '2025': None,
            }
            for path in paths:
                self.assertFalse(path.is_dir(), msg='Directory already exists')

            self.worker.make_directories(paths.keys())

            for path in paths:
                self.assertTrue(path.is_dir())

    def test_flatten_plan(self) -> None:
        plan = {
            Path('here'): [
                planner.Map(source=Path('neither'), destination=Path('here')),
                planner.Map(source=Path('nor'), destination=Path('there')),
            ],
            Path('other'): [planner.Map(source=Path('a'), destination=Path('b'))],
        }
        self.assertEqual(
            [
                planner.Map(source=Path('neither'), destination=Path('here')),
                planner.Map(source=Path('nor'), destination=Path('there')),
                planner.Map(source=Path('a'), destination=Path('b')),
            ],
            self.worker.flatten_plan(plan),
        )
