import pathlib


class Renamer:
    def get_output_path(self, file_info):
        return self.get_filepath(file_info) / self.get_filename(file_info)

    def get_filepath(self, file_info):
        """Create a file path based on the capture date (with fallback for creation date)"""
        file_date = file_info.get_creation_datetime()
        file_path = file_date.strftime('%Y/%m/%y%m%d')
        return pathlib.Path(file_path)

    def get_filename(self, file_info):
        """Try to create a unique filename for each photo"""
        if file_info.camera_model and file_info.shutter_count:
            return f'{file_info.camera_serial}_{file_info.shutter_count:>06}{file_info.extension}'

        return file_info.original_name
