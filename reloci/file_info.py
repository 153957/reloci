import contextlib

from datetime import datetime, timezone

TAGS = [
    'Composite:SubSecDateTimeOriginal',
    'EXIF:DateTimeOriginal',
    'EXIF:Make',
    'EXIF:Model',
    'MakerNotes:DateTimeOriginal',
    'MakerNotes:SerialNumber',
    'MakerNotes:ShutterCount',
]


class FileInfo:
    def __init__(self, path, exiftool):
        self.file = path
        self.tags = exiftool.get_tags(str(path), TAGS)[0]

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
    def camera_make(self):
        return str(self.tags.get('EXIF:Make', ''))

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

        Assume UTC timezone when not available from EXIF.

        """
        with contextlib.suppress(KeyError):
            date_time_original = self.tags['Composite:SubSecDateTimeOriginal']
            try:
                return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S.%f%z')
            except ValueError:
                return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S.%f').replace(tzinfo=timezone.utc)

        with contextlib.suppress(KeyError):
            date_time_original = self.tags['MakerNotes:DateTimeOriginal']
            try:
                return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S%z')
            except ValueError:
                return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S').replace(tzinfo=timezone.utc)

        with contextlib.suppress(KeyError):
            date_time_original = self.tags['EXIF:DateTimeOriginal']
            try:
                return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S%z')
            except ValueError:
                return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S').replace(tzinfo=timezone.utc)

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
