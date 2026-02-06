import unittest

from pathlib import Path

from exiftool import ExifToolHelper

from reloci import file_info


class FileInfoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.image_path = Path(__file__).parent.parent / 'demo/source/APL_082158.NEF'
        self.movie_path = Path(__file__).parent.parent / 'demo/source/IMG_9895.MOV'
        with ExifToolHelper() as exiftool:
            self.image_info = file_info.FileInfo(self.image_path, exiftool)
            self.movie_info = file_info.FileInfo(self.movie_path, exiftool)

    def test_init(self) -> None:
        self.assertEqual(self.image_path, self.image_info.file)
        self.assertIsInstance(self.image_info.tags, dict)

    def test_extension(self) -> None:
        self.assertEqual('.NEF', self.image_info.extension)
        self.assertEqual('.MOV', self.movie_info.extension)

    def test_camera_make(self) -> None:
        self.assertEqual('NIKON CORPORATION', self.image_info.camera_make)
        self.assertEqual('Apple', self.movie_info.camera_make)

    def test_original_name(self) -> None:
        self.assertEqual('APL_082158.NEF', self.image_info.original_name)
        self.assertEqual('IMG_9895.MOV', self.movie_info.original_name)

    def test_file_stat(self) -> None:
        self.assertEqual(17479594, self.image_info.file_stat.st_size)
        self.assertEqual(1392448, self.movie_info.file_stat.st_size)

    def test_camera_model(self) -> None:
        self.assertEqual('NIKON D500', self.image_info.camera_model)
        self.assertEqual('iPhone SE', self.movie_info.camera_model)

    def test_camera_serial(self) -> None:
        self.assertEqual('6037845', self.image_info.camera_serial)
        with self.assertRaises(LookupError):
            _ = self.movie_info.camera_serial

    def test_shutter_count(self) -> None:
        self.assertEqual('82158', self.image_info.shutter_count)
        with self.assertRaises(LookupError):
            _ = self.movie_info.shutter_count

    def test_subsecond_datetime(self) -> None:
        self.assertEqual('2021-04-02T13:00:02.670000+00:00', self.image_info.subsecond_datetime.isoformat())
        with self.assertRaises(LookupError):
            self.movie_info.subsecond_datetime.isoformat()

    def test_datetime(self) -> None:
        self.assertEqual('2021-04-02T13:00:02+00:00', self.image_info.date_time.isoformat())
        self.assertEqual('2020-03-20T16:35:52+01:00', self.movie_info.date_time.isoformat())

    def test_creation_datetime(self) -> None:
        self.assertNotEqual('2021-04-02T13:00:02.670000+00:00', self.image_info.creation_datetime.isoformat())
        self.assertNotEqual('2021-04-02T13:00:02.670000+00:00', self.movie_info.creation_datetime.isoformat())
