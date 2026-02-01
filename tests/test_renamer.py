import datetime
import unittest

from pathlib import Path
from unittest import mock

from reloci import renamer


class RenamerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.renamer = renamer.Renamer()

    def test_encode_timestamp(self) -> None:
        with self.subTest('Timestamp accureate to whole seconds'):
            self.assertEqual(
                '5o6aq40',
                self.renamer.encode_timestamp(timestamp=12345678),
            )

        with self.subTest('Timestamp with milliseconds'):
            self.assertEqual(
                '5o6aq7f',
                self.renamer.encode_timestamp(timestamp=12345678.123),
            )

        with self.subTest('Does not support sub-milliseconds'):
            self.assertEqual(
                '5o6aq7f',
                self.renamer.encode_timestamp(timestamp=12345678.1234),
            )

    def test_replace_prefix(self) -> None:
        self.assertEqual('APL_6795628.NEF', self.renamer.replace_prefix('6037845_6795628.NEF'))
        self.assertEqual('TRM_6795628.HEIC', self.renamer.replace_prefix('iPhone 13 mini_6795628.HEIC'))

    def test_get_filepath(self) -> None:
        file_info = mock.Mock()
        file_info.date_time = datetime.datetime(2020, 2, 2, 20, 2, 2, tzinfo=datetime.UTC)
        self.assertEqual(Path('2020/02/200202'), self.renamer.get_filepath(file_info))

        file_info.date_time = datetime.datetime(2012, 3, 14, 9, 11, 34, tzinfo=datetime.UTC)
        self.assertEqual(Path('2012/03/120314'), self.renamer.get_filepath(file_info))

    def test_get_fallback_filepath(self) -> None:
        file_info = mock.Mock()
        file_info.date_time.strftime = mock.PropertyMock(side_effect=LookupError)
        self.assertEqual(Path('0000/00/000000'), self.renamer.get_fallback_filepath(file_info))

    def test_get_filename(self) -> None:
        file_info = mock.Mock()
        file_info.original_name = 'DSC_0001.NEF'
        file_info.shutter_count = 15395
        file_info.camera_serial = '6037845'
        file_info.extension = '.NEF'
        self.assertEqual('APL_015395.NEF', self.renamer.get_filename(file_info))

    def test_get_suffix(self) -> None:
        """Identify on-device editted files and mark them as such."""
        file_info = mock.Mock()

        file_info.original_name = 'IMG_E1539.HEIC'
        self.assertEqual('_edited', self.renamer.get_suffix(file_info))

        file_info.original_name = 'TRM_153934_edited.HEIC'
        self.assertEqual('_edited', self.renamer.get_suffix(file_info))

        file_info.original_name = 'IMG_1539.HEIC'
        self.assertEqual('', self.renamer.get_suffix(file_info))
