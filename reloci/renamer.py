import pathlib


class Renamer:
    def get_output_path(self, file_info):
        file_date = file_info.get_creation_datetime()
        file_path = file_date.strftime('%Y/%m/%y%m%d')
        return pathlib.Path(file_path) / file_info.file.name
