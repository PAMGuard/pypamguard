from contextlib import contextmanager
import io
import time

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

class PAMGuardFile(Serializable):
    """
    This class represents a PAMGuard Binary File
    """
    
    def __init__(self, path: str, fp: io.BufferedReader, order: BYTE_ORDERS = BYTE_ORDERS.BIG_ENDIAN, module_registry: ModuleRegistry = ModuleRegistry(), filters: Filters = Filters()):
        """
        :param filename: The name of the file
        :param fp: The file pointer
        :param order: Override byte order of the file (optional)
        :param module_registry: Override the module registry (optional)
        :param filters: The filters (optional)
        """
        self.report = Report()
        self.__path: str = path
        self.__filename = os.path.basename(self.__path)
        self.__fp: io.BufferedReader = fp
        self.__order: BYTE_ORDERS = order
        self.__module_registry: ModuleRegistry = module_registry
        self.__filters: Filters = filters
        self.__module_class: GenericModule # will be overriden by module registry
        self.__size: int = self.__get_size()
        self.total_time: int = 0

        self.__file_header: GenericFileHeader = StandardFileHeader()
        self.__module_header: GenericModuleHeader = None
        self.__module_footer: GenericModuleFooter = None
        self.__file_footer: GenericFileFooter = StandardFileFooter(self.__file_header)
        self.__data: list[GenericModule] = []
        self.__background: list[GenericBackground] = []

    def __process_chunk(self, br: BinaryReader, chunk_obj: BaseChunk, chunk_info: GenericChunkInfo, correct_chunk_length = True):
        try:
            if type(chunk_info) in (GenericModule, GenericBackground) and self.__filters.position == FILTER_POSITION.STOP: raise FilterMismatchException()
            logger.debug(f"Processing chunk: {type(chunk_obj)}", br)
            chunk_obj.process(br, chunk_info)
            if not br.at_checkpoint(): raise ChunkLengthMismatch(br, chunk_info, chunk_obj)
        except WarningException as e:
            self.report.add_warning(e)
        except FilterMismatchException as e:
            br.goto_checkpoint()
            return None
        except CriticalException as e:
            raise e
        except Exception as e:
            self.report.add_error(e)
        if correct_chunk_length and not br.at_checkpoint(): br.goto_checkpoint()
        return chunk_obj

    def __get_size(self):
        temp = self.__fp.tell()
        self.__fp.seek(0, io.SEEK_END)
        size = self.__fp.tell()
        self.__fp.seek(temp, io.SEEK_SET)
        return size

    def load(self):
        start_time = time.time()
        self.__fp.seek(0, io.SEEK_SET)
        data_count = 0
        bg_count = 0

        while True:
            br = BinaryReader(self.__fp, report = self.report)
            if br.tell() == self.__size: break
            
            # each chunk has the same 8-byte 'chunk info' at the start
            chunk_info = StandardChunkInfo()
            chunk_info.process(br)
            br.set_checkpoint(chunk_info.length - chunk_info._measured_length)

            logger.debug(f"Reading chunk of type {chunk_info.identifier} and length {chunk_info.length} at offset {br.tell()}", br)

            if chunk_info.identifier == IdentifierType.FILE_HEADER.value:
                self.report.set_context(self.__file_header)
                self.__file_header = self.__process_chunk(br, self.__file_header, chunk_info, correct_chunk_length=False)
                self.__module_class = self.__module_registry.get_module(self.__file_header.module_type, self.__file_header.stream_name)

            elif chunk_info.identifier == IdentifierType.MODULE_HEADER.value:
                self.report.set_context(self.__module_header)
                if not self.__file_header: raise StructuralException(self.__fp, "File header not found before module header")
                self.__module_header = self.__process_chunk(br, self.__module_class._header(self.__file_header), chunk_info)

            elif chunk_info.identifier >= 0:
                self.report.set_context(f"{self.__module_class} [iter {data_count}]")
                if not self.__module_header: raise StructuralException(self.__fp, "Module header not found before data")
                data = self.__process_chunk(br, self.__module_class(self.__file_header, self.__module_header, self.__filters), chunk_info)
                if data: self.__data.append(data)
                data_count += 1
                
            elif chunk_info.identifier == IdentifierType.MODULE_FOOTER.value:
                self.report.set_context(self.__module_footer)
                if not self.__module_header: raise StructuralException(self.__fp, "Module header not found before module footer")
                self.__module_footer = self.__process_chunk(br, self.__module_class._footer(self.__file_header, self.__module_header), chunk_info)

            elif chunk_info.identifier == IdentifierType.FILE_FOOTER.value:
                self.report.set_context(self.__file_footer)
                if not self.__file_header: raise StructuralException(self.__fp, "File header not found before file footer")
                self.__file_footer = self.__process_chunk(br, self.__file_footer, chunk_info)

            elif chunk_info.identifier == IdentifierType.FILE_BACKGROUND.value:
                self.report.set_context(f"{self.__module_class._background} [iter {bg_count}]")
                if not self.__module_header: raise StructuralException(self.__fp, "Module header not found before data")
                if self.__module_class._background is None: raise StructuralException(self.__fp, "Module class does not have a background specified")
                background = self.__process_chunk(br, self.__module_class._background(self.__file_header, self.__module_header, self.__filters), chunk_info)
                if background: self.__background.append(background)
                bg_count += 1

            elif chunk_info.identifier == IdentifierType.IGNORE.value:
                br.goto_checkpoint()

            else:
                raise StructuralException(self.__fp, f"Unknown chunk identifier: {chunk_info.identifier}")
                
        self.total_time = time.time() - start_time
        logger.info("File processed in %.2f ms" % (self.total_time * 1000))

    def to_json(self):
        return {
            "filters": self.filters.to_json() if self.filters else None,
            "file_header": self.__file_header.to_json() if self.__file_header else None,
            "module_header": self.__module_header.to_json() if self.__module_header else None,
            "module_footer": self.__module_footer.to_json() if self.__module_footer else None,
            "file_footer": self.__file_footer.to_json() if self.__file_footer else None,
            "data": [chunk.to_json() for chunk in self.__data] if self.__data else [],
            "background": [chunk.to_json() for chunk in self.__background] if self.__background else [],
        }

    def __str__(self):
        ret = f"PAMGuard Binary File (filename={self.__path}, size={self.size} bytes, order={self.__order})\n\n"
        ret += f"{self.__filters}\n"
        ret += f"{self.report}"
        ret += f"File Header\n{self.__file_header}\n\n"
        ret += f"Module Header\n{self.__module_header}\n\n"
        ret += f"Module Footer\n{self.__module_footer}\n\n"
        ret += f"File Footer\n{self.__file_footer}\n\n"
        ret += f"Data Set: {len(self.__data)} objects\n"
        ret += f"Total time: {self.total_time:.2f} seconds\n"
        return ret
    
    @property
    def size(self):
        return self.__size

    @property
    def file_header(self):
        return self.__file_header
    
    @property
    def module_header(self):
        return self.__module_header
    
    @property
    def module_footer(self):
        return self.__module_footer
    
    @property
    def file_footer(self):
        return self.__file_footer

    @property
    def filters(self):
        return self.__filters
    
    @property
    def module_class(self):
        return self.__module_class
    
    @property
    def order(self):
        return self.__order
    
    @property
    def path(self):
        return self.__path
    
    @property
    def module_registry(self):
        return self.__module_registry
    
    @property
    def data(self):
        return self.__data

    @property
    def background(self):
        return self.__background