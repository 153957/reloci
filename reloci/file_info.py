import contextlib

from datetime import datetime

TAGS = [
    'Composite:SubSecDateTimeOriginal',
    'EXIF:DateTimeOriginal',
    'EXIF:Model',
    'MakerNotes:DateTimeOriginal',
    'MakerNotes:SerialNumber',
    'MakerNotes:ShutterCount',
]


class FileInfo:
    def __init__(self, path, exiftool):
        self.file = path
        self.tags = exiftool.get_tags(TAGS, str(path))

    @property
    def extension(self):
        return self.file.suffix

    @property
    def original_name(self):
        return self.file.name

    @property
    def file_stat(self):
        return self.file.stat()

    @property
    def camera_model(self):
        return str(self.tags.get('EXIF:Model', ''))

    @property
    def camera_serial(self):
        return str(self.tags.get('MakerNotes:SerialNumber', ''))

    @property
    def shutter_count(self):
        return str(self.tags.get('MakerNotes:ShutterCount', ''))

    @property
    def exif_datetime(self):
        """Extract original capture date from EXIF

        Try to get an accurate time by including the subsecond component.
        Raises LookupError if the date is not available in EXIF.

        """
        with contextlib.suppress(KeyError):
            date_time_original = self.tags['Composite:SubSecDateTimeOriginal']
            return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S.%f')

        with contextlib.suppress(KeyError):
            date_time_original = self.tags['MakerNotes:DateTimeOriginal']
            return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S')

        with contextlib.suppress(KeyError):
            date_time_original = self.tags['EXIF:DateTimeOriginal']
            return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S')

        raise LookupError(f'Did not find original date in EXIF of {self.file}')

    @property
    def creation_datetime(self):
        """Extract file creation date

        These times are not always accurate file created dates.
        Implementation also differ between operating systems.

        """
        try:
            timestamp = self.file_stat.st_birthtime
        except AttributeError:
            timestamp = self.file_stat.st_ctime
        return datetime.fromtimestamp(timestamp)
