Version: {{ version }}

This guide is an overview and explains the important features. Details are found in the PyPAMGuard api reference.

## Getting Started

### What is PyPAMGuard

PyPAMGuard is a package for processing PAMGuard binary file outputs in Python. [PAMGuard](https://www.pamguard.org/) is a software program written in [Java](https://www.java.com/en/) that has a number of applications related to passive acoustic monitoring. Most modules produce binary files names _pamguard data files_ (.pgdf) which follow a core standard structure defined in the PAMGuard source code. The PyPAMGuard library can read these data files into python data types and objects that allow users to further process the data however they wish.

Users may prefer to use the [MATLAB or R ](https://www.pamguard.org/matlabandr.html) binary file readers should they be more comfortable with these languages.

### What is a PGDF

A PAMGuard Data File (PGDF) is produced by a PAMGuard _module_. A standard PGDF must contain the following chunk types, in order:

- **File Header** (1 exactly) contains metadata about the file and the module within it (structure is identical across all PGDFs)
- **Module Header** (1 exactly) contains metadata about the data of the module (structure is module-dependent)
- **Data Set** (0 or more) contains the data itself (structure is module-dependent)
- **Module Footer** (1 exactly) contains further metadata about the data of the module (structure is module-dependent)
- **File Footer** (1 exactly) contains metadata about the file (structure is identical across all PGDFs)

If you want to learn more about how these files are produced, please inspect the PAMGuard source code. You can also learn more about the specific attributes in each of these chunks by loading a PGDF using this library (see: Quick Start).

### Installation

Before proceeding, ensure you have Python installed on your local Windows, Linux or MacOS system.

#### Python Package Index

You can install PyPAMGuard from the [Python Package Index](https://pypi.org/) using the following command.
```
pip install pypamguard
```

### Quick Start

Processing a data file using PyPAMGuard is as easy as importing the library, and calling one function, passing in the path to the data file. 

```python
# file.py
import pypamguard
df = pypamguard.load_pamguard_binary_file('path/to/data/file.pgdf')
```

You can then access the file headers and footers from the object like so.

```python
df.file_info.file_header # file header
df.file_info.module_header # module header
df.file_info.module_footer # module footer
df.file_info.file_footer # file footer
```

Access the module data itself like so.

```python
len(df.data) # number of module data chunks
df.data[0] # the first module data chunk
```

All headers, footers, and module data, contain attributes that were read from the binary file. For example, each file header will **always** contain a `version`. This can intuitively be accessed like an attribute of an object. Some example are shown below.

```python
df.file_info.file_header.version # integer
df.file_info.file_header.module_type # bytes
```

You can access a detailed list of all attributes of each chunk by converting it to a string and/or printing it. Exact attributes of each header, footer or module data chunk are not listed in this README as they may change in between file versions. It is recommended to run the library yourself on a particular data file and find the attributes yourself.

```python
print(df.file_info.file_header)

# OUTPUT
#
# File Header
#         length (<class 'int'>): 103
#         identifier (<class 'int'>): -1
#         file_format (<class 'int'>): 0
#         pamguard (<class 'bytes'>): b'PAMGUARDDATA'
#         version (<class 'bytes'>): b'1.15.03'
#         branch (<class 'bytes'>): b'BETA'
#         data_date (<class 'datetime.datetime'>): 2016-09-03 00:42:14+00:00
#         analysis_date (<class 'datetime.datetime'>): 2016-10-27 19:43:26.511000+00:00
#         start_sample (<class 'int'>): 0
#         module_type (<class 'bytes'>): b'Click Detector'
#         module_name (<class 'bytes'>): b'Click Detector'
#         stream_name (<class 'bytes'>): b'Clicks'
#         extra_info_len (<class 'int'>): 0
```

See the extended README file below, and the API reference for more information on data types, filtering, and creating your own modules.

## Customisation

### Logger Verbosity

PyPAMGuard has its own logging capabilities to Python's standard output stream. You can pass in an argument `verbosity` to `load_pamguard_binary_file` using a class of imported enums from `pypamguard.logger` (see below).

```python
import pypamguard
from pypamguard.logger import logger, Verbosity
logger.set_verbosity(Verbosity.DEBUG)
pypamguard.load_pamguard_binary_file('path/to/data/file.pgdf')
```

The `Verbosity` enum that can be imported from `pypamguard.logger` can be set to the following values:

- `Verbosity.DEBUG` print debug info, info, warnings and errors
- `Verbosity.INFO` print info, warnings and errors
- `Verbosity.WARNING` print warnings and errors
- `Verbosity.ERROR` print errors

### Filtering

PyPAMGuard allows you to filter data as it is being streamed into its internal data structures. This offers various speed and memory efficiencies, particularly with large data files. To do this, you must pass in a `Filters` object from `pypamguard.core.filters` as shown below.

```python
from pypamguard.core.filters import Filters
from pypamguard import load_pamguard_binary_file

filters = Filters()
df = load_pamguard_binary_file('path/to/data/file.pgdf', filters=filters)
```

An empty `Filters` object will have no effect on filtering. The following filters were defined at the time of writing this documentation, however you can access the most up-to-date list by printing `pypamguard.core.filters.Filters.INSTALLED_FILTERS`.

```python
{
    'uidlist': <class 'pypamguard.core.filters.WhitelistFilter'>,
    'uidrange': <class 'pypamguard.core.filters.RangeFilter'>,
    'daterange': <class 'pypamguard.core.filters.DateFilter'>
}
```

#### UID List Filter

Filtering by whitelist allows you to define a specific list of values that can be accepted.

```python
from pypamguard.core.filters import Filter, WhitelistFilter
from pypamguard import load_pamguard_binary_file
filters = Filters({
    'uidlist': WhitelistFilter([1,2,3,10])
})
load_pamguard_binary_file('path/to/data/file.pgdf', filters=filters)
```

#### UID Range Filter

A range filter is a kind of filter that takes a start and end point, and includes all the date between these (inclusive). Define a range filter like so.

> WARNING: passing `ordered=True` will cause data chunks to be skipped once the first item out of the upper bound is reached, so is dangerous to use on unordered or unknown data.

```python
from pypamguard.core.filters import Filters, RangeFilter
from pypamguard import load_pamguard_binary_file
filters = Filters({
    'uidlist': RangeFilter(start=1, end=10, ordered=False)
})
load_pamguard_binary_file('path/to/data/file.pgdf', filters=filters)
```

#### Date Range Filter

Filtering by date range is similar to filtering by generic range, except you pass in `datetime.datetime` objects to the constructor of the filter. Note that the datetime objects must contain UTC timezone information, otherwise the filter will throw a `ValueError` exception.

```python
from pypamguard.core.filters import Filters, DateFilter
from pypamguard import load_pamguard_binary_file
import datetime

from_timestamp: datetime.datetime # some UTC datetime object
to_timestamp: datetime.datetime # some UTC datetime object

filters = Filters({
    'daterange': DateFilter(from_timestamp, to_timestamp, ordered=True)
})
load_pamguard_binary_file('path/to/data/file.pgdf', filters=filters)
```

### Custom Filter

Define a custom filter function which is run once each chunk is loaded.
Use the template below for this.

```python
from pypamguard.core.filters import Filters, FILTER_POSITION
from pypamguard.chunks.standard import StandardModule
from pypamguard import load_pamguard_binary_file

def custom_filter(data: StandardModule):
    if data.uid == 10:
        # Keep UID 10
        return FILTER_POSITION.KEEP
    elif data.uid < 10:
        # Skip all chunks before UID 10
        return FILTER_POSITION.SKIP
    elif data.uid > 11:
        # Stop executing at UID 12
        return FILTER_POSITION.STOP
    # Keep UID 11 (as returning None is the
    # same as returning FILTER_POSITION.KEEP

filters = Filters()
filters.add_custom_filter(custom_filter)
load_pamguard_binary_file('path/to/data/file.pgdf', filters=filters)
```

## Fundamentals

### Data Types

Headers, footers and module data automatically read data into their _native_ (or close to) Python data types, to allow for easy use. 

Python-core and standard third-party data types are:

- `int` (whole numbers)
- `float` (decimal numbers)
- `bytes` (strings) 
- `datetime.datetime` (dates and times)
- `numpy.array` (arrays of ints or floats)

PyPAMGuard has its own `core.Bitmap` class which is used to abstract the reading and processing of integer bitmap flags. A brief example is given below on how to interact with a Bitmap, but more information can be found in the API reference.

```python
import pypamguard
# the 4-bit representation of 2 in binary is 0010
bm = pypamguard.utils.bitmap.Bitmap(size=4, value=2) 
bm.get_set_bits() # returns [1]
bm.set(3) # sets bit 3
bm.get_set_bits() # returns [1, 3]
bm.clear(1) # clears bit 1
bm.get_set_bits() # returns [3] 
```