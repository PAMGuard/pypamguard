from __future__ import annotations

import copy
import glob
from pathlib import Path

from pypamguard.chunks.generics import GenericModule, GenericBackground
from pypamguard.load_pamguard_binary_file import load_pamguard_binary_file
from pypamguard.core.pamguardfile import PAMGuardFile
from pypamguard.core.filters import FILTER_POSITION, Filters
from pypamguard.core.readers import Report
import os

from pypamguard.logger import logger


def load_pamguard_binary_folder(directory: str | Path, mask: str, clear_fields: list = None, filters: Filters = None, report: Report = None) -> tuple[list[GenericModule], list[GenericBackground], Report]:
    r"""
    A function to load a number of PAMGuard binary files from a directory. Returns a tuple containing an array
    of `pypamguard.chunks.generics.genmodule.GenericModule` (data) objects and a list of `pypamguard.chunks.generics.genbackground.GenericBackground`
     (background) objects. Each of the data and background objects contain an attribute `file_info` containing a pointer
     to the `pypamguard.core.pamguardfile.FileInfo` object pertaining to that data/background chunk.
    Set the verbosity beforehand using `pypamguard.logger.Logger.set_verbosity`.

    ```python
    from pypamguard.logger import logger, Verbosity
    logger.set_verbosity(Verbosity.WARNING) # ignore INFO and DEBUG
    ```

    Example usage:

    ```python
    from pypamguard import load_pamguard_binary_folder
    data, background, report = load_pamguard_binary_folder("path/to/directory/", "*.pgdf")
    ```

    Example usage with an ordered filter:

    ```python
    import datetime
    from pypamguard import load_pamguard_binary_folder
    from pypamguard.core.filters import Filters, DateFilter
    filter_obj = Filters({"daterange": DateFilter(start_date=datetime.datetime(2022, 1, 1, tz = datetime.UTC), end_date=datetime.datetime(2022, 1, 2, tz = datetime.UTC), ordered=True)})
    data, background, report = load_pamguard_binary_folder("path/to/directory/", "*.pgdf", filters=filter_obj)
    ```

    :param directory: The directory containing the PAMGuard binary files
    :param mask: A glob mask to filter the files to load (e.g. '\*.pgdf' to match all files with the .pgdf extension, or '\*\*/\*.pgdf' to match all files with the .pgdf extension in any subdirectory)
    :param clear_fields: A list of fields to clear from the PAMGuardFile object. These fields will be set to None. This might be useful if you want to remove unecessary data from the PAMGuardFile object.
    :param filters: A `core.filters.Filters` object. Can be None.
    :param report: A `core.readers.Report` object. Can be None.
    """

    data = []
    background = []

    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory {directory} does not exist.")
    if not report:
        report = Report()

    files = glob.glob(pathname=mask, root_dir=directory, recursive=True)
    for idx, file in enumerate(files):
        filter_copy = copy.deepcopy(filters)
        res = load_pamguard_binary_file(
            os.path.join(directory, file),
            filters=filter_copy,
            report=report,
            clear_fields=clear_fields,
            )
        res.add_file_info()
        data.extend(res.data)
        background.extend(res.background)
        logger.info(f"Processed files: {idx + 1}")
        if res.filters.position == FILTER_POSITION.STOP: break

    return data, background, report
