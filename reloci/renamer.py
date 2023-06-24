from contextlib import suppress
from pathlib import Path

import baseconv

from reloci.file_info import FileInfo


class BaseRenamer:
    def get_output_path(self, file_info: FileInfo) -> Path:
        """Placeholder method to indicate this should be implemented

        An implementation of get_output_path gets FileInfo for the file being renamed
        as argument and must return the new path, as a pathlib.Path object.

        """
        raise NotImplementedError('This method must be implemented.')

    def get_fallback_output_path(self, file_info: FileInfo) -> Path:
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

    def get_output_path(self, file_info: FileInfo) -> Path:
        return self.get_filepath(file_info) / file_info.original_name

    def get_fallback_output_path(self, file_info: FileInfo) -> Path:
        return self.get_output_path(file_info)

    def get_filepath(self, file_info: FileInfo) -> Path:
        """Create a file path based on the capture date (with fallback for creation date)"""
        file_path = file_info.date_time.strftime('%Y/%m/%y%m%d')
        return Path(file_path)


class DateTimeRenamer(BaseRenamer):
    """Rename files based on exif date

    The resulting file path will be:

        '%Y/%m/%y%m%d/%Y%m%d_%H%M%S_%f.{extension}'

    For example:

        '2021/07/210723/20210723_110242_351000.NEF'

    """

    def get_output_path(self, file_info: FileInfo) -> Path:
        return self.get_filepath(file_info) / self.get_filename(file_info)

    def get_fallback_output_path(self, file_info: FileInfo) -> Path:
        return self.get_output_path(file_info)

    def get_filepath(self, file_info: FileInfo) -> Path:
        """Create a file path based on the capture date (with fallback for creation date)"""
        file_path = file_info.date_time.strftime('%Y/%m/%y%m%d')
        return Path(file_path)

    def get_filename(self, file_info: FileInfo) -> str:
        """Try to create a unique filename for each photo"""
        try:
            return file_info.subsecond_datetime.strftime(f'%Y%m%d_%H%M%S_%f{file_info.extension}')
        except LookupError:
            return file_info.date_time.strftime(f'%Y%m%d_%H%M%S_%f{file_info.extension}')


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

    def encode_timestamp(self, timestamp: float) -> str:
        microsecond_timestamp = int(1_000 * timestamp)
        encoded_timestamp: str = baseconv.base36.encode(microsecond_timestamp)
        return encoded_timestamp

    def replace_prefix(self, name: str) -> str:
        return (
            name
            # Serial numbers
            .replace('2225260_', 'ADL_')
            .replace('4019215_', 'WEN_')
            .replace('4020135_', 'DSC_')
            .replace('6037845_', 'APL_')
            .replace('6795628_', 'ARN_')
            # Camera models
            .replace('Canon PowerShot S60_', 'S60_')
            .replace('NIKON D500_', 'APS_')
            .replace('NIKON D90_', 'ARM_')
            .replace('iPhone 5_', 'CBG_')
            .replace('iPhone 13 mini_', 'TRM_')
            .replace('iPhone SE_', 'CLK_')
            .replace('iPhone SE (1st generation)_', 'CLK_')
            .replace('iPad Pro (10.5-inch)_', 'PAD_')
            # Other
            .replace('6023198_', 'TED_')
            .replace('6040831_', 'KIM_')
        )

    def get_output_path(self, file_info: FileInfo) -> Path:
        return self.get_filepath(file_info) / self.get_filename(file_info)

    def get_fallback_output_path(self, file_info: FileInfo) -> Path:
        return self.get_fallback_filepath(file_info) / self.get_fallback_filename(file_info)

    def get_filepath(self, file_info: FileInfo) -> Path:
        """Create a file path based on the capture date (with fallback for EXIF creation date)"""
        file_path = file_info.date_time.strftime('%Y/%m/%y%m%d')
        return Path(file_path)

    def get_fallback_filepath(self, file_info: FileInfo) -> Path:
        """Try the accurate filepath, if that fails fallback to zeroes"""
        with suppress(LookupError):
            return self.get_filepath(file_info)

        return Path('0000/00/000000')

    def get_filename(self, file_info: FileInfo) -> str:
        """Try to create a unique filename for each photo"""
        suffix = self.get_suffix(file_info)

        with suppress(LookupError):
            return self.replace_prefix(
                f'{file_info.camera_serial}_{file_info.shutter_count:>06}{suffix}{file_info.extension}',
            )

        encoded_timestamp = self.encode_timestamp(file_info.subsecond_datetime.timestamp())
        return self.replace_prefix(f'{file_info.camera_model}_{encoded_timestamp}{suffix}{file_info.extension}')

    def get_fallback_filename(self, file_info: FileInfo) -> str:
        """Try to create a unique filename for each photo"""
        with suppress(LookupError):
            return self.get_filename(file_info)

        suffix = self.get_suffix(file_info)

        with suppress(LookupError):
            encoded_timestamp = self.encode_timestamp(file_info.date_time.timestamp())
            return self.replace_prefix(f'{file_info.camera_model}_{encoded_timestamp}{suffix}{file_info.extension}')

        return file_info.original_name

    def get_suffix(self, file_info: FileInfo) -> str:
        """Determine if an additional suffix should be added to the name"""
        if 'IMG_E' in file_info.original_name:
            # Image was edited on iOS
            return '_edited'

        if '_edited' in file_info.original_name:
            # Image was previously suffixed, keep the suffix
            return '_edited'

        return ''
