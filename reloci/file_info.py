from datetime import datetime


class FileInfo:
    def __init__(self, path):
        self.file = path

    @property
    def file_stat(self):
        return self.file.stat()

    def get_creation_datetime(self):
        timestamp = self.file_stat.st_ctime
        return datetime.fromtimestamp(timestamp)
