import time
from pypamguard.core.pamguardfile import PAMGuardFile
from pypamguard.utils.constants import BYTE_ORDERS, DEFAULT_BUFFER_SIZE
from pypamguard.core.filters import Filters, DateFilter
from .logger import logger, Verbosity, logger_config
import io, json
from contextlib import contextmanager
import time

@contextmanager
def timer(label):
    logger.debug(f"Started {label}")
    start_time = time.perf_counter()
    yield
    total_time = time.perf_counter() - start_time
    logger.debug(f"Finished {label} in {total_time:.3f} seconds")

def load_pamguard_binary_file(filename, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN, buffering: int | None = DEFAULT_BUFFER_SIZE, verbosity: Verbosity = Verbosity.INFO, filters: Filters = Filters(), json_path: str = None) -> PAMGuardFile:
    """
    Read a binary PAMGuard data file into a PAMFile object
    :param filename: absolute or relative path to the .pgdt file to read
    :param order: endianess of data (defaults to 'network')
    :param buffering: number of bytes to buffer
    :param verbosity: logger verbosity level
    :param filters: filters to apply to data
    :param json_path: write json to a specific path
    """

    with logger_config(verbosity=verbosity):
        with timer("loading PAMGuard binary file"):
            with open(filename, "rb", buffering=buffering) as f:
                pgbfile = PAMGuardFile(path=filename, fp=f, order=order, filters=filters)
                pgbfile.load()
        if json_path:
            with open(json_path, 'w') as output:
                # logger.start_progress_bar(limit=100, name="Writing JSON output", unit="MB", scale=1/1024 ** 2, rounding=2, show_info=False)
                json_data = json.dumps(pgbfile.to_json(), indent=0, separators=(",", ": "))
                json_size = len(json_data.encode())
                # logger.update_progress_bar(limit=json_size, show_info=True)
                with timer(f"writing output JSON to {output.name}"):
                    output.write(json_data)
                # logger.log_progress(json_size)
    return pgbfile

