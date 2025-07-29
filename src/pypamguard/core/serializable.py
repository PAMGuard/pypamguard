from abc import ABC, abstractmethod
import numpy as np
import datetime
from pypamguard.utils.bitmap import Bitmap

class Serializable(ABC):
    
    def serialize(self, value):

        if issubclass(type(value), Serializable):
            return value.to_json()

        if isinstance(value, (list, set, np.ndarray)):
            if len(value) == 0: return value
            return [self.serialize(i) for i in value]
        if isinstance(value, np.floating): # remove floating point precision errors#
            return round(float(value), np.finfo(value.dtype).precision)
        if type(value) == datetime.datetime: return value.timestamp()
        if type(value) == Bitmap: return value.bits
        if isinstance(value, (int, float, str, bool, type(None))): return value
        elif isinstance(value, np.generic): return value.item()
        return str(value)
    

    def to_json(self):
        return {**{attr: self.serialize(value) for attr, value in self.__dict__.items() if not attr.startswith('_')}, "__name__": self.__class__.__name__}

    @classmethod
    def from_json(cls, json):
        raise NotImplementedError
