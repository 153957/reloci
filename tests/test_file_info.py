import unittest

from pathlib import Path

from exiftool import ExifToolHelper

from reloci import file_info


class FileInfoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.image_path = Path(__file__).parent.parent / 'demo/source/APL_082158.NEF'
        with ExifToolHelper() as exiftool:
            self.info = file_info.FileInfo(self.image_path, exiftool)

    def test_init(self) -> None:
        self.assertEqual(self.image_path, self.info.file)
        self.assertIsInstance(self.info.tags, dict)

    def test_extension(self) -> None:
        self.assertEqual('.NEF', self.info.extension)

    def test_original_name(self) -> None:
        self.assertEqual('APL_082158.NEF', self.info.original_name)

    def test_file_stat(self) -> None:
        self.assertEqual(17479594, self.info.file_stat.st_size)

    def test_camera_model(self) -> None:
        self.assertEqual('NIKON D500', self.info.camera_model)

    def test_camera_serial(self) -> None:
        self.assertEqual('6037845', self.info.camera_serial)

    def test_shutter_count(self) -> None:
        self.assertEqual('82158', self.info.shutter_count)

    def test_subsecond_datetime(self) -> None:
        self.assertEqual('2021-04-02T13:00:02.670000+00:00', self.info.subsecond_datetime.isoformat())

    def test_datetime(self) -> None:
        self.assertEqual('2021-04-02T13:00:02+00:00', self.info.date_time.isoformat())

    def test_creation_datetime(self) -> None:
        self.assertNotEqual('2021-04-02T13:00:02.670000', self.info.creation_datetime.isoformat())
