# Contributing Guidelines

pypamguard is an open-source project. Whilst our license does not require it, we welcome you
to contribute any changes you make back to the original repository. 

## Getting Started

If you are planning on making contributions to pypamguard, we highly recommend that you
fork the repository into your own GitHub profile. Once you fork the repository, and have
cloned it onto your machine, getting started is
relatively simple. You should create and run a virtual environment, then install all
the requirements in [requirements.txt] via pip. This will install pypamgaurd's core
packages, as well as additional tools such as pytest.

On Windows
```commandline
python -m venv venv
venv\Scripts\activate.bat
pip install requirements.txt
```

On Linux/Mac

```commandline
python -m venv venv
source venv/bin/activate
pip install requirements.txt
```

The best way to run pypamguard is as a python module.
You can do this by creating or using an 'entry file'
such as [src/pypamguard/main.py](src/pypamguard/main.py)
and calling this like so.

```commandline
cd src
python -m pypamguard.main
```

Alternatively, you can run a python interpreter in your
console.

```commandline
cd src
python
```

And then run pypamguard as you would any other module
```python
import pypamguard
pypamguard.load_pamguard_binary_file(...)
```

## Testing

There is a comprehensive testing suite located in the
[tests](tests) folder. To run these tests, in the root
directory of the repository, run the following command.

```commandline
pytest
```

If you add new functionality to PyPAMGuard, please ensure
you write appropriate unit tests in pytest to give other
developers peace-of-mind when making changes to the code
base. If you are modifying old features of PyPAMGUard
it is a good idea to run the existing tests to ensure that
the interface does not change.

> If you find that changes you have made are failing
> existing tests (due to an existing bug in the program or
> testing suite), you are welcome to change the testing suite.

## Making a Pull Request

Once you are satisfied with your tested changes, you
should make a pull request, linking an issue and with
a detailed commit history (if there is one), changelog,
and details and any new tests written. 

The GitHub repository will automatically run the unit
tests in MacOS, Linux, and Windows - and you can see
this by viewing your pull request.

## Creating a New Release

Stable code is made available through releases. This
allows users to download the soruce code from the 
releases page on the GitHub repository. Upon the
creation of a release, the following CI actions are
executed (allow 1 - 3 minutes for these to complete):

1. The user-facing code (README.md, LICENSE, src/*)
is put in an archive and attached to the release. 
2. A wheel and tarball of the archive are sent to
PyPI.

Releases should be semantically named and tagged like
so. These tags are dynamically inserted in the tarball
and wheel uploaded to PyPI.

- V1.2.3
  - Tag: v1.2.3
- V1.2.3 Beta 1
  - Tag: v1.2.3-b1
- V1.2.3 Alpha 1
  - Tag: v1.2.3-a1

> Semantic versioning is crucial for the automated
> integration with PyPI.

## Sample Code

> PyPAMGuard is heavily object oriented. Thanks to this
> it is made to be modular and extensible. We have included
> some basic information below about the structure of the
> codebase and how to easily extend it.

There are three main folders in [src/pypamguard](src/pypamguard).

- [chunks](src/pypamguard/chunks) contains classes for generic, standard
    and custom modules.
- [core](src/pypamguard/core) contains classes and functions for business-
    level logic and management of the chunks (contains
    [pamguardfile.py](src/pypamguard/core/pamguardfile.py) which is the main
    entry-point.
- [utils](src/pypamguard/utils) contains generic helpers that are used by
    core and chunks.

> Check out the main helper function in [load_pamguard_binary_file](src/pypamguard/load_pamguard_binary_file.py)
> which culminates in an instantiation of a PAMGuardFile object.

### Adding Modules

```python
# custommodule.py
from pypamguard.chunks.standard import StandardModule, StandardModuleHeader, StandardModuleFooter, StandardBackground
from pypamguard.core.readers import *

class CustomModule(StandardModule):

    def __init__(self, file_header, module_header, filters):
        super().__init__(file_header, module_header, filters)
        
        # INSERT FIELD INITIALIZATIONS HERE
        self.field1: np.int64 = None
        self.field2: Bitmap = None
        self.field3: np.float32 = None
        self.field4: np.ndarray = np.array([])
    
    def _process(self, br, chunk_info):
        super()._process(br, chunk_info)

        # INSERT MODULE LOGIC HERE (this is automatically
        # executed after the standard module data.
```

You may wish to add custom module header, module footer
or background logic. You can do this by defining new classes
using the template below. Note that these share a common
superclass with the `StandardModule` above provided a very
similar interface.

```python

from pypamguard.chunks.standard import StandardModuleFooter, StandardModuleHeader, StandardBackground
from pypamguard.core.readers import *

class CustomModuleHeader(StandardModuleHeader):
    
    def __init__(self, file_header, *args, **kwargs):
        super().__init__(file_header, *args, **kwargs)
        # <-- FIELD INITIALIZATIONS -->

    def _process(self, br: BinaryReader, chunk_info):
        # <-- MODULE LOGIC -->
        pass


class CustomModuleFooter(StandardModuleFooter):

    def __init__(self, file_header, module_header):
        super().__init__(file_header, module_header)
        # <-- FIELD INITIALIZATIONS -->

    def _process(self, br, chunk_info):
        # <-- MODULE LOGIC -->
        pass

class CustomBackground(StandardBackground):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # <-- FIELD INITIALIZATIONS -->

    def _process(self, br, chunk_info):
        super()._process(br, chunk_info)
        # <-- MODULE LOGIC -->
```

Make sure you import these custom chunk types
into the custom module you build above.

```python
class CustomModule(StandardModule):
    
    _header = CustomModuleHeader
    _footer = CustomModuleFooter
    _background = CustomModuleBackground
```

Finally, you need to register your module in
[core/registry.py](src/pypamguard/core/registry.py).

```python
from pypamguard.chunks.modules.custommodule import CustomModule
MODULES = {
    # <-- CURRENT ATTRIBUTES -->
    "Custom Stream Name": CustomModule,
}
```

## Exceptions

PyPAMGuard has a custom suite of exceptions in 
[core/exceptions](src/pypamguard/core/exceptions.py).
Throwing exceptions like Python's standard ValueError
will cause an exception that terminates PyPAMGuard.
You should control these modules by throwing subclasses
of `WarningException` or `WarningError` for non-destructive
warnings or errors you want to be added to the report for
the user. 
