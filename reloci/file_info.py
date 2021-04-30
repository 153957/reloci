from datetime import datetime

import exifreader


class FileInfo:
    def __init__(self, path):
        self.file = path

        with self.file.open('rb') as _file:
            self.tags = exifreader.process_file(_file, details=True)

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
        return str(self.tags.get('Image Model', ''))

    @property
    def camera_serial(self):
        return str(self.tags.get('MakerNote SerialNumber', ''))

    @property
    def shutter_count(self):
        return str(self.tags.get('MakerNote TotalShutterReleases', ''))

    @property
    def exif_datetime(self):
        """Extract original capture date from EXIF

        Try to get an accurate time by including the subsecond component.
        Raises KeyError if the date is not available in EXIF.

        """
        date_time = self.tags['EXIF DateTimeOriginal']
        subsec = self.tags.get('EXIF SubSecTimeOriginal', '0')
        full_date_time = f'{date_time}.{subsec}'
        return datetime.strptime(full_date_time, '%Y:%m:%d %H:%M:%S.%f')

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
