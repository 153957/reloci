import datetime
import pathlib

from operator import attrgetter

from exiftool import ExifToolHelper
from rich.progress import track

from reloci.file_info import FileInfo

MARGIN = datetime.timedelta(seconds=0.2)
MIN_INTERVAL = datetime.timedelta(seconds=0.4)
MIN_IMAGES_SEQUENCE = 20


def find_sequences(pattern: str, shots_per_interval: int, group: bool) -> None:
    skip = shots_per_interval
    files = sorted(pathlib.Path().glob(pattern))

    if len(files) <= MIN_IMAGES_SEQUENCE:
        print(f'Found no files matching the pattern "{pattern}"')
        return

    with ExifToolHelper() as exiftool:
        image_dates = sorted(
            (FileInfo(path, exiftool) for path in track(files[::skip], description='Reading dates')),
            key=attrgetter('subsecond_datetime'),
        )

    start_of_sequence = image_dates[0].file
    sequence = [start_of_sequence]
    nth_sequence = 1

    print(
        ' seq',
        '   n',
        'interval',
        'sequence',
        sep='\t',
    )

    for previous, current, following in zip(image_dates[:-2], image_dates[1:-1], image_dates[2:], strict=True):
        sequence.append(current.file)

        interval = current.subsecond_datetime - previous.subsecond_datetime
        new_interval = following.subsecond_datetime - current.subsecond_datetime

        if interval < MIN_INTERVAL or abs(interval - new_interval) > MARGIN:
            if len(sequence) > MIN_IMAGES_SEQUENCE:
                print(
                    f'{nth_sequence:4}',
                    f'{len(sequence):4}',
                    f'{interval.total_seconds():7}s',
                    f'{sequence[0]} → {sequence[-1]}',
                    sep='\t',
                )
                if group:
                    group_sequence(sequence, nth_sequence)
                nth_sequence += 1
            sequence = [current.file]

    sequence.append(following.file)
    if len(sequence) > MIN_IMAGES_SEQUENCE:
        print(
            f'{nth_sequence:4}',
            f'{len(sequence):4}',
            f'{new_interval.total_seconds():7}s',
            f'{sequence[0]} → {sequence[-1]}',
            sep='\t',
        )
        if group:
            group_sequence(sequence, nth_sequence)


def group_sequence(sequence: list[pathlib.Path], sequence_number: int) -> None:
    """Group all files in the sequence into a subdirectory in the working directory"""

    pathlib.Path(f'sequence_{sequence_number}').mkdir()
    for path in sequence:
        path.rename(f'sequence_{sequence_number}/{path.name}')
