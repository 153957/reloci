import pathlib

from contextlib import suppress

import baseconv


class BaseRenamer:
    def get_output_path(self, file_info):
        """Placeholder method to indicate this should be implemented

        An implementation of get_output_path gets FileInfo for the file being renamed
        as argument and must return the new path, as a pathlib.Path object.

        """
        raise NotImplementedError('This method must be implemented.')

    def get_fallback_output_path(self, file_info):
        """Placeholder method to indicate this should be implemented

        An implementation of get_fallback_output_path gets FileInfo for the file being renamed
        as argument and must return the new path, as a pathlib.Path object.

        """
        raise NotImplementedError('This method must be implemented.')


class DatePathRenamer(BaseRenamer):
    """Do not rename files, but group them by date

    The resulting file path will be:

        '%Y/%m/%y%m%d/{original_name}'

    For example:

        '2021/07/210723/DSC_7346.NEF'

    """
    def get_output_path(self, file_info):
        return self.get_filepath(file_info) / file_info.original_name

    def get_fallback_output_path(self, file_info):
        return self.get_output_path(file_info)

    def get_filepath(self, file_info):
        """Create a file path based on the capture date (with fallback for creation date)"""
        file_path = file_info.datetime.strftime('%Y/%m/%y%m%d')
        return pathlib.Path(file_path)


class DateTimeRenamer(BaseRenamer):
    """Rename files based on exif date

    The resulting file path will be:

        '%Y/%m/%y%m%d/%Y%m%d_%H%M%S_%f.{extension}'

    For example:

        '2021/07/210723/20210723_110242_351000.NEF'

    """

    def get_output_path(self, file_info):
        return self.get_filepath(file_info) / self.get_filename(file_info)

    def get_fallback_output_path(self, file_info):
        return self.get_output_path(file_info)

    def get_filepath(self, file_info):
        """Create a file path based on the capture date (with fallback for creation date)"""
        file_path = file_info.datetime.strftime('%Y/%m/%y%m%d')
        return pathlib.Path(file_path)

    def get_filename(self, file_info):
        """Try to create a unique filename for each photo"""
        try:
            return file_info.subsecond_datetime.strftime(f'%Y%m%d_%H%M%S_%f{file_info.extension}')
        except LookupError:
            return file_info.datetime.strftime(f'%Y%m%d_%H%M%S_%f{file_info.extension}')


class Renamer(BaseRenamer):
    """Rename files based on camera serial and shutter count or model and encoded timestamp

    The resulting file path will be:

        '%Y/%m/%y%m%d/{prefix}_{shutter}.{extension}'
        '%Y/%m/%y%m%d/{prefix}_{encoded_timestamp}.{extension}'
        '%Y/%m/%y%m%d/{original_name}'

    For example:

        '2021/07/210723/APL_042107.NEF'
        '2020/03/200320/CLK_k80cid1l.JPG'
        '2021/07/210723/APS_8297.MOV'

    """
    def encode_timestamp(self, timestamp):
        microsecond_timestamp = int(1000 * timestamp)
        encoded_timestamp = baseconv.base36.encode(microsecond_timestamp)
        return encoded_timestamp

    def replace_prefix(self, name):
        return (
            name
            # Serial numbers
            .replace('2225260_', 'ADL_')
            .replace('4019215_', 'WEN_')
            .replace('4020135_', 'DSC_')
            .replace('6037845_', 'APL_')
            .replace('6795628_', 'ARN_')
            .replace('6023198_', 'TED_')
            .replace('6040831_', 'KIM_')
            # Camera models
            .replace('Canon PowerShot S60_', 'S60_')
            .replace('NIKON D500_', 'APS_')
            .replace('NIKON D90_', 'ARM_')
            .replace('iPhone 13 mini_', 'TRM_')
            .replace('iPhone SE_', 'CLK_')
            .replace('iPhone SE (1st generation)_', 'CLK_')
            .replace('iPad Pro (10.5-inch)_', 'PAD_')
        )

    def get_output_path(self, file_info):
        return self.get_filepath(file_info) / self.get_filename(file_info)

    def get_fallback_output_path(self, file_info):
        return self.get_filepath(file_info) / self.get_fallback_filename(file_info)

    def get_filepath(self, file_info):
        """Create a file path based on the capture date (with fallback for creation date)"""
        file_path = file_info.datetime.strftime('%Y/%m/%y%m%d')
        return pathlib.Path(file_path)

    def get_filename(self, file_info):
        """Try to create a unique filename for each photo"""
        with suppress(LookupError):
            return self.replace_prefix(
                f'{file_info.camera_serial}_{file_info.shutter_count:>06}{file_info.extension}'
            )

        encoded_timestamp = self.encode_timestamp(file_info.subsecond_datetime.timestamp())
        return self.replace_prefix(
            f'{file_info.camera_model}_{encoded_timestamp}{file_info.extension}'
        )

    def get_fallback_filename(self, file_info):
        """Try to create a unique filename for each photo"""
        with suppress(LookupError):
            encoded_timestamp = self.encode_timestamp(file_info.datetime.timestamp())
            return self.replace_prefix(
                f'{file_info.camera_model}_{encoded_timestamp}{file_info.extension}'
            )

        return file_info.original_name
