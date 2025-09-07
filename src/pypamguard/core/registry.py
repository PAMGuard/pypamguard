"""
A package for registering custom PAMGuard modules, and registering in-built
PAMGuard modules. See `ModuleRegistry`. Effectively
a registration is a mapping from a module name (and possible stream) to a 
class found in `pypamguard.chunks.modules`. When a file header is read, the
registry is used to load the correct module class corresponding to the module
type specified in the header.

`MODULES` dict includes all default mappings. Any
nested dict is a stream-specification rather than just module name.
"""

from pypamguard.chunks.generics import GenericModule
from pypamguard.core.exceptions import ModuleNotFoundException
from pypamguard.logger import logger

from pypamguard.chunks.modules.processing.ais import AISProcessing
__ais_config = AISProcessing

from pypamguard.chunks.modules.detectors.click import ClickDetector
from pypamguard.chunks.modules.detectors.clicktriggerbackground import ClickTriggerBackground
__click_config = {
    "Clicks": ClickDetector,
    "Trigger Background": ClickTriggerBackground,
}

from pypamguard.chunks.modules.processing.clipgenerator import ClipGenerator
__clipgenerator_config = ClipGenerator

from pypamguard.chunks.modules.classifiers.deeplearningclassifier import DLCDetections, DLCModels
__deeplearningclassifier_config = {
    "DL_detection": DLCDetections,
    "DL detection": DLCDetections,
    "DL_Model_Data": DLCModels,
    "DL Model Data": DLCModels,
}

from pypamguard.chunks.modules.processing.dbht import DbHtProcessing
__dbht_config = DbHtProcessing

from pypamguard.chunks.modules.processing.difar import DIFARProcessing
__difar_config = DIFARProcessing

from pypamguard.chunks.modules.processing.noisemonitor import NoiseMonitor
__noisemonitor_config = NoiseMonitor

from pypamguard.chunks.modules.processing.noiseband import NoiseBandMonitor
__noiseband_config = NoiseBandMonitor

from pypamguard.chunks.modules.detectors.gpl import GPLDetector
__gpl_config = GPLDetector

from pypamguard.chunks.modules.detectors.rwedge import RWEdgeDetector
__rwedge_config = RWEdgeDetector

from pypamguard.chunks.modules.detectors.whistleandmoan import WhistleAndMoanDetector
__whistleandmoan_config = WhistleAndMoanDetector

from pypamguard.chunks.modules.processing.longtermspectralaverage import LongTermSpectralAverage
__longtermspectralaverage_config = LongTermSpectralAverage

from pypamguard.chunks.modules.processing.ishmael import IshmaelData, IshmaelDetections
__ishmael_config = {
    "Ishmael Peak Data": IshmaelData, # Not currently output from the detector
    "Ishmael Detections": IshmaelDetections,
}

from pypamguard.chunks.modules.plugins.spermwhaleipi import SpermWhaleIPI
__spermwhaleipi_config = SpermWhaleIPI

from pypamguard.chunks.modules.plugins.geminithreshold import GeminiThresholdDetector
__geminithreshold_config = GeminiThresholdDetector

MODULES = {
    "AIS Processing": __ais_config,
    "Click Detector": __click_config,
    "SoundTrap Click Detector": __click_config,
    "Clip Generator": __clipgenerator_config,
    "Deep Learning Classifier": __deeplearningclassifier_config,
    "DbHt": __dbht_config,
    "DIFAR Processing": __difar_config,
    "LTSA": __longtermspectralaverage_config,
    "Noise Monitor": __noisemonitor_config,
    "Noise Band": __noisemonitor_config,
    "NoiseBand": __noiseband_config,
    "GPL Detector": __gpl_config,
    "RW Edge Detector": __rwedge_config,
    "WhistlesMoans": __whistleandmoan_config,
    "Energy Sum Detector": __ishmael_config,
    "Spectrogram Correlation Detector": __ishmael_config,
    "Matched Filter Detector": __ishmael_config,
    "Ipi module": __spermwhaleipi_config,
    "Gemini Threshold Detector": __geminithreshold_config,
}

class ModuleRegistry:
    """
    A class which stores mappings from module types and streams to module classes
    found in `pypamguard.chunks.modules` (or custom user-defined modules). All
    default modules are in `MODULES`. Usually a module registry is automatically
    created when a `PAMGuard` file is opened. The only time that you might need to
    pass your own `ModuleRegistry` in is when creating custom modules.
    """

    def __init__(self):
        self.modules: dict[str, GenericModule | dict[str, GenericModule]] = {}
        self.__register_preinstalled_modules()

    def register_module(self, module_name: str, module_class: GenericModule | dict):
        """
        Register a new module.
        
        If a module is valid for all streams, then
        ```python
        registry.register_module("Module Type", ModuleClass)
        ```
        
        If a module is stream-specific, then
        ```python
        registry.register_module("Module Type", {"Stream A": ModuleClass, "Stream B": ModuleClass})
        ```
        """
        if module_name in self.modules:
            raise ValueError(f"Module {module_name} is already registered. Deregister module first by calling `deregister_module('{module_name}')`.")
        self.modules[module_name] = module_class
    
    def deregister_module(self, module_name: str) -> int:
        """Deregister a module. Returns the number of modules deregistered (either 0 or 1)"""
        if module_name in self.modules:
            del self.modules[module_name]
            return 1
        return 0
    
    def get_module(self, module_name: str, module_stream) -> GenericModule:
        if module_name in self.modules and type(self.modules[module_name]) == dict:
            if module_stream in self.modules[module_name]: return self.modules[module_name][module_stream]
            raise ModuleNotFoundException(f"Module '{module_name}' is not registered for stream '{module_stream}'.")
        elif module_name in self.modules and issubclass(self.modules[module_name], GenericModule):
            return self.modules[module_name]
        elif module_name in self.modules:
            raise ModuleNotFoundException(f"Module '{module_name}' is not registered correctly.")
        else:
            raise ModuleNotFoundException(f"Module '{module_name}' is not registered.")

    def __register_preinstalled_modules(self):
        for module in MODULES:
            self.register_module(module, MODULES[module])
