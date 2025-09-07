import os
from pathlib import Path
from pypamguard.core.pamguardfile import PAMGuardFile
from pypamguard.utils.constants import BYTE_ORDERS, DEFAULT_BUFFER_SIZE
from pypamguard.core.filters import Filters, DateFilter
from pypamguard.core.readers import Report
from .logger import logger, Verbosity, logger_config
import io, json
from pypamguard.utils.timer import timer

def load_pamguard_binary_file(filename: str | Path, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN, buffering: int | None = DEFAULT_BUFFER_SIZE, filters: Filters = None, json_path: str = None, report: Report = None, clear_fields = None) -> PAMGuardFile:
    """
    Read a binary PAMGuard data file into a PAMFile object

    ```python
    import pypamguard
    file = pypamguard.load_binary_data_file('path/to/data/file.pgdf')
    print(file.file_info.file_header)
    print(file.file_info.module_header)
    print(file.file_info.file_footer)
    print(file.file_info.module_footer)
    print(file.data[0])
    ```

    :param filename: absolute or relative path to the .pgdt file to read
    :param order: endianness of data
    :param buffering: number of bytes to buffer
    :param filters: filters to apply to data
    :param json_path: write json to a specific path
    :param report: report object to use for logging
    :param clear_fields: list of fields to remove from data objects in the PAMGuardFile (for memory)
    :return: PAMGuardFile
    """
    if filters is None: filters = Filters()

    with timer("loading PAMGuard binary file"):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exist")
        with open(filename, "rb", buffering=buffering) as f:
            f = PAMGuardFile(path=filename, fp=f, order=order, filters=filters, report=report, clear_fields=clear_fields)
            f.load()
    if json_path:
        with open(json_path, 'w') as output:
            json_data = json.dumps(f.to_json(), indent=0, separators=(",", ": "))
            with timer(f"writing output JSON to {output.name}"):
                output.write(json_data)
    return f

