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

    def get_creation_datetime(self):
        if self.tags:
            date_time = self.tags['EXIF DateTimeOriginal']
            subsec = self.tags.get('EXIF SubSecTimeOriginal', '0')
            full_date_time = f'{date_time}.{subsec}'
            image_date = datetime.strptime(full_date_time, '%Y:%m:%d %H:%M:%S.%f')
        else:
            # Fallback to file creation date if no EXIF is available
            timestamp = self.file_stat.st_ctime
            image_date = datetime.fromtimestamp(timestamp)

        return image_date
