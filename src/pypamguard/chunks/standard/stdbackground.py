from pypamguard.chunks.annotations.annotationmanager import AnnotationManager
from pypamguard.chunks.generics.genbackground import GenericBackground
from pypamguard.chunks.standard import StandardModuleHeader, StandardFileHeader, StandardModule, StandardChunkInfo
from pypamguard.core.readers import *
from pypamguard.core.filters import Filters
from pypamguard.chunks.standard.stddata import StandardDataMixin

class StandardBackground(GenericBackground, StandardDataMixin):
    def __init__(self, file_header, module_header, filters,  *args, **kwargs):
        super().__init__(file_header, module_header, filters, *args, **kwargs)
        self._initialize_stddata()
        self.annotations: AnnotationManager = None


    def _process(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        super()._process(br, chunk_info)
        self._process_stddata(br, chunk_info)

    def _post(self, br: BinaryReader, chunk_info: StandardChunkInfo):
        super()._post(br)
        if self.flag_bitmap.is_set("HASBINARYANNOTATIONS"):
            self.annotations = AnnotationManager()
            self.annotations.process(br)