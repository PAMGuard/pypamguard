from contextlib import contextmanager
import io
import time, typing

from pypamguard.core.exceptions import BinaryFileException, WarningException, CriticalException, ChunkLengthMismatch, StructuralException
from pypamguard.chunks.base import BaseChunk
from pypamguard.chunks.standard import StandardBackground, StandardChunkInfo, StandardFileHeader, StandardFileFooter, StandardModuleHeader, StandardModuleFooter
from pypamguard.chunks.generics import GenericBackground, GenericChunkInfo, GenericFileHeader, GenericFileFooter, GenericModuleHeader, GenericModuleFooter, GenericModule
from pypamguard.core.registry import ModuleRegistry
from pypamguard.utils.constants import IdentifierType
from pypamguard.utils.constants import BYTE_ORDERS
from pypamguard.core.filters import Filters, FILTER_POSITION, FilterMismatchException
from pypamguard.logger import logger, Verbosity
from pypamguard.core.serializable import Serializable
from pypamguard.core.readers import *
import os

class FileInfo(Serializable):
    def __init__(self):
        self.__file_header = None
        self.__module_header = None
        self.__module_footer = None
        self.__file_footer = None

    @property
    def file_header(self):
        return self.__file_header

    @file_header.setter
    def file_header(self, file_header: GenericFileHeader):
        self.__file_header = file_header

    @property
    def module_header(self):
        return self.__module_header

    @module_header.setter
    def module_header(self, module_header: GenericModuleHeader):
        self.__module_header = module_header

    @property
    def module_footer(self):
        return self.__module_footer

    @module_footer.setter
    def module_footer(self, module_footer: GenericModuleFooter):
        self.__module_footer = module_footer

    @property
    def file_footer(self):
        return self.__file_footer

    @file_footer.setter
    def file_footer(self, file_footer: GenericFileFooter):
        self.__file_footer = file_footer

class PAMGuardFile(Serializable):
    """
    This class represents a PAMGuard Binary File
    """
    
    def __init__(self, path: str, fp: typing.BinaryIO, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN, module_registry: ModuleRegistry = ModuleRegistry(), filters: Filters = Filters(), report: Report = None, clear_fields=None):
        """
        Initialize a PAMGuardFile object. This will set-up the binary reader, but
        not actually read any data yet. See `load()`.

        :param path: The path of the file (this is only used for logging)
        :param fp: The file pointer from which data is read (must be opened with 'rb' mode)
        :param order: Override byte order of the file (optional)
        :param module_registry: Override the module registry (optional)
        :param filters: The filters passed as a `core.filters.Filters` object (optional)
        :param report: A `core.readers.Report` object used for logging (optional)
        """
        if report is None: self.report = Report()
        else: self.report = report
        self.__file_info = FileInfo()
        self.__file_info.file_header = StandardFileHeader()
        self.__file_info.file_footer = StandardFileFooter(self.__file_info.file_header)
        self.__path: str = path
        self.__filename = os.path.basename(self.__path)
        self.__fp: io.BufferedReader = fp
        self.__order: BYTE_ORDERS = order
        self.__module_registry: ModuleRegistry = module_registry
        self.__filters: Filters = filters
        self.__module_class: GenericModule.__class__ = None # will be overriden by module registry
        self.__size: int = self.__get_size()

        self.__data: list[GenericModule] = []
        self.__background: list[GenericBackground] = []
        self.__total_time: int = 0
        self.__clear_fields = clear_fields

    def __process_chunk(self, br: BinaryReader, chunk_obj: BaseChunk, chunk_info: GenericChunkInfo, correct_chunk_length = True):
        try:
            logger.debug(f"Processing chunk: {type(chunk_obj)}", br)
            chunk_obj.process(br, chunk_info)
            if issubclass(type(chunk_obj), (GenericModule, GenericBackground)):
                if self.__filters.position == FILTER_POSITION.KEEP:
                    self.__filters.call_custom_filters(chunk_obj)
                if self.__filters.position == FILTER_POSITION.STOP:
                    raise FilterMismatchException()
            if not br.at_checkpoint(): raise ChunkLengthMismatch(br, chunk_info, chunk_obj)
        except WarningException as e:
            self.report.add_warning(e)
        except FilterMismatchException as e:
            br.goto_checkpoint()
            return None
        except CriticalException as e:
            raise e
        except ErrorException as e:
            self.report.add_error(e)
        except Exception as e:
            raise e
        if correct_chunk_length and not br.at_checkpoint(): br.goto_checkpoint()
        return chunk_obj

    def __get_size(self):
        temp = self.__fp.tell()
        self.__fp.seek(0, io.SEEK_END)
        size = self.__fp.tell()
        self.__fp.seek(temp, io.SEEK_SET)
        return size

    def load(self) -> None:
        """
        Load the PAMGuard Binary File, restarting the `fp` (file pointer) from
        the constructor at the beginning. You can see any warnings or errors using
        the `report` (`pypamguard.core.readers.Report`) attribute.

        Throws a `pypamguard.core.exceptions.BinaryFileException` (or a subclass thereof) if
        something goes wrong.
        """

        start_time = time.time()
        self.__fp.seek(0, io.SEEK_SET)
        data_count = 0
        bg_count = 0

        while True:
            br = BinaryReader(self.__fp, report = self.report)
            if br.tell() == self.__size: break
            
            # each chunk has the same 8-byte 'chunk info' at the start
            chunk_info = StandardChunkInfo(self.__path)
            chunk_info.process(br)
            br.set_checkpoint(chunk_info.length - chunk_info.measured_length)

            logger.debug(f"Reading chunk of type {chunk_info.identifier} and length {chunk_info.length} at offset {br.tell()}", br)

            if chunk_info.identifier == IdentifierType.FILE_HEADER.value:
                self.report.set_context(self.__file_info.file_header.__class__)
                self.__file_info.file_header = self.__process_chunk(br, self.__file_info.file_header, chunk_info, correct_chunk_length=False)
                self.__module_class = self.__module_registry.get_module(self.__file_info.file_header.module_type, self.__file_info.file_header.stream_name)

            elif chunk_info.identifier == IdentifierType.MODULE_HEADER.value:
                self.report.set_context(self.__file_info.module_header.__class__)
                if not self.__file_info.file_header: raise StructuralException(self.__fp, "File header not found before module header")
                self.__file_info.module_header = self.__process_chunk(br, self.__module_class._header(self.__file_info.file_header), chunk_info)

            elif chunk_info.identifier >= 0:
                self.report.set_context(f"{self.__module_class.__class__} [iter {data_count}]")
                if not self.__file_info.module_header: raise StructuralException(self.__fp, "Module header not found before data")
                data = self.__process_chunk(br, self.__module_class(self.__file_info.file_header, self.__file_info.module_header, self.__filters), chunk_info)
                if self.__clear_fields and data:
                    for f in self.__clear_fields:
                        data.__dict__.pop(f, None)
                if data: self.__data.append(data)
                data_count += 1
                
            elif chunk_info.identifier == IdentifierType.MODULE_FOOTER.value:
                self.report.set_context(self.__file_info.module_footer.__class__)
                if not self.__file_info.module_header: raise StructuralException(self.__fp, "Module header not found before module footer")
                self.__file_info.module_footer = self.__process_chunk(br, self.__module_class._footer(self.__file_info.file_header, self.__file_info.module_header), chunk_info)

            elif chunk_info.identifier == IdentifierType.FILE_FOOTER.value:
                self.report.set_context(self.__file_info.file_footer.__class__)
                if not self.__file_info.file_header: raise StructuralException(self.__fp, "File header not found before file footer")
                self.__file_info.file_footer = self.__process_chunk(br, self.__file_info.file_footer, chunk_info)

            elif chunk_info.identifier == IdentifierType.FILE_BACKGROUND.value:
                self.report.set_context(f"{self.__module_class._background.__class__} [iter {bg_count}]")
                if not self.__file_info.module_header: raise StructuralException(self.__fp, "Module header not found before data")
                if self.__module_class._background is None: raise StructuralException(self.__fp, "Module class does not have a background specified")
                background = self.__process_chunk(br, self.__module_class._background(self.__file_info.file_header, self.__file_info.module_header, self.__filters), chunk_info)
                if background: self.__background.append(background)
                bg_count += 1

            elif chunk_info.identifier == IdentifierType.IGNORE.value:
                br.goto_checkpoint()

            else:
                raise StructuralException(self.__fp, f"Unknown chunk identifier: {chunk_info.identifier}")
                
        self.__total_time = time.time() - start_time

    def to_json(self):
        return {
            "filters": self.filters.to_json() if self.filters else None,
            "file_header": self.__file_info.file_header.to_json() if self.__file_info.file_header else None,
            "module_header": self.__file_info.module_header.to_json() if self.__file_info.module_header else None,
            "module_footer": self.__file_info.module_footer.to_json() if self.__file_info.module_footer else None,
            "file_footer": self.__file_info.file_footer.to_json() if self.__file_info.file_footer else None,
            "data": [chunk.to_json() for chunk in self.__data] if self.__data else [],
            "background": [chunk.to_json() for chunk in self.__background] if self.__background else [],
        }

    def __str__(self):
        ret = f"PAMGuard Binary File (filename={self.__path}, size={self.__size} bytes, order={self.__order})\n\n"
        ret += f"{self.__filters}\n"
        ret += f"{self.report}"
        ret += f"File Header\n{self.__file_info.file_header}\n\n"
        ret += f"Module Header\n{self.__file_info.module_header}\n\n"
        ret += f"Module Footer\n{self.__file_info.module_footer}\n\n"
        ret += f"File Footer\n{self.__file_info.file_footer}\n\n"
        ret += f"Data Set: {len(self.__data)} objects\n"
        ret += f"Total time: {self.__total_time:.2f} seconds\n"
        return ret

    def add_file_info(self):
        for data in self.__data:
            data.file_info = self.__file_info
        for background in self.__background:
            background.file_info = self.__file_info

    @property
    def background(self) -> list[GenericBackground]:
        """The background data of the PAMGuard file"""
        return self.__background

    @property
    def data(self) -> list[GenericModule]:
        """The data of the PAMGuard file"""
        return self.__data

    @property
    def filters(self) -> Filters:
        """The filters used when processing the PAMGuard file"""
        return self.__filters

    @property
    def path(self) -> str:
        """The path of the PAMGuard file"""
        return self.__path

    @property
    def file_info(self) -> FileInfo:
        """The file info of the PAMGuard file (headers and footers)"""
        return self.__file_info