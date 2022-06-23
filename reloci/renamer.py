import pathlib

import baseconv


class BaseRenamer:
    def get_output_path(self, file_info):
        """Placeholder method to indicate this should be implemented

        An implementation of get_output_path gets FileInfo for the file being renamed
        as argument and must return the new path, as a pathlib.Path object.

        """
        raise NotImplementedError('This method must be implemented.')


class DateTimeRenamer(BaseRenamer):
    """Rename files based on exif date

    The resulting file path will be:

        '%Y/%m/%d/%Y%m%d_%H%M%S_%f.{extension}'

    For example:

        '2021/07/23/20210723_110242_351000.NEF'

    """

    def get_output_path(self, file_info):
        return self.get_filepath(file_info) / self.get_filename(file_info)

    def get_filepath(self, file_info):
        """Create a file path based on the capture date (with fallback for creation date)"""
        file_path = file_info.exif_datetime.strftime('%Y/%m/%y%m%d')
        return pathlib.Path(file_path)

    def get_filename(self, file_info):
        """Try to create a unique filename for each photo"""
        return file_info.exif_datetime.strftime(f'%Y%m%d_%H%M%S_%f{file_info.extension}')


class Renamer(BaseRenamer):
    def get_output_path(self, file_info):
        return self.get_filepath(file_info) / self.get_filename(file_info)

    def get_filepath(self, file_info):
        """Create a file path based on the capture date (with fallback for creation date)"""
        file_path = file_info.exif_datetime.strftime('%Y/%m/%y%m%d')
        return pathlib.Path(file_path)

    def get_filename(self, file_info):
        """Try to create a unique filename for each photo"""
        if file_info.camera_model and file_info.shutter_count:
            return (
                f'{file_info.camera_serial}_{file_info.shutter_count:>06}{file_info.extension}'
                .replace('2225260_', 'ADL_')
                .replace('4019215_', 'WEN_')
                .replace('4020135_', 'DSC_')
                .replace('6037845_', 'APL_')
                .replace('6795628_', 'ARN_')
                .replace('6023198_', 'TED_')
            )
        elif file_info.camera_make == 'Apple':
            timestamp = int(1000 * file_info.exif_datetime.timestamp())
            encoded_timestamp = baseconv.base36.encode(timestamp)
            return (
                f'{file_info.camera_model}_{encoded_timestamp}{file_info.extension}'
                .replace('iPhone 13 mini_', 'TRM_')
                .replace('iPhone SE_', 'CLK_')
                .replace('iPhone SE (1st generation)_', 'CLK_')
                .replace('iPad Pro (10.5-inch)_', 'PAD_')
            )

        return file_info.original_name
