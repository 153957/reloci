import tempfile
import unittest

from pathlib import Path

from reloci import check_interval


class CheckIntervalTest(unittest.TestCase):
    def test_group_sequence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_path = Path(tmp_dir)
            temp_files = [temp_path / f'DSC_{i}.NEF' for i in range(10)]
            for temp_file in temp_files:
                temp_file.touch()
            check_interval.group_sequence(
                temp_files,
                sequence_number=123,
            )
            self.assertTrue((temp_path / 'sequence_123').is_dir())
            self.assertEqual(1, len(list(temp_path.iterdir())))
            self.assertEqual(10, len(list((temp_path / 'sequence_123').iterdir())))
