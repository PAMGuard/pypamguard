import datetime
import enum
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Callable
from pypamguard.core.serializable import Serializable

class FilterMismatchException(Exception):
    """
    Raised when a filter is applied to a value and is not met. It is automatically
    thrown by the `Filters` class.
    """
    pass

class FILTER_POSITION(enum.Enum):
    SKIP = 0 # ignore this object but keep reading
    KEEP = 1 # include this object
    STOP = 2 # ignore this, and all following objects

class BaseFilter(Serializable, ABC):
    """Base class for all filters."""

    @abstractmethod
    def check(self, value) -> FILTER_POSITION:
        """
        Apply the filter to the value and return either `KEEP`, `SKIP` or `STOP`
        from the `FILTER_POSITION` enum. 
        """
        raise NotImplementedError

    @classmethod
    def from_json(self, json):
        name = json.pop("__name__")
        if name == "WhitelistFilter":
            return WhitelistFilter.from_json(json)
        elif name == "RangeFilter":
            return RangeFilter.from_json(json)
        elif name == "DateFilter":
            return DateFilter.from_json(json)
        else:
            raise NotImplementedError(f"Implement the .from_json() method for the {name} filter to deserialize from JSON.")

class WhitelistFilter(BaseFilter):
    """A filter that checks if a value is in a set of whitelisted values."""

    def __init__(self, whitelist: set | list):
        """
        Pass in an unordered list or a set of values to include in the whitelist.
        @param whitelist: A list or set of values to include in the whitelist.
        """
        self.whitelist = set(whitelist)

    def check(self, value):
        if value in self.whitelist:
            return FILTER_POSITION.KEEP
        return FILTER_POSITION.SKIP

    def __str__(self):
        return f"WhitelistFilter({len(self.whitelist)} elements)"

    @classmethod
    def from_json(cls, json):
        self = cls(whitelist=set(json["whitelist"]))
        return self

class RangeFilter(BaseFilter):
    def __init__(self, start, end, comparator=None, validation_func=None, ordered=False, ignore_none=False):
        """
        Process a value and return KEEP either when the value is between the start and end values.
        Return SKIP or STOP when the value is outside the range, depending on the ordered flag.

        @param start: The start value of the range.
        @param end: The end value of the range.
        @param comparator: A function that takes two values and returns a boolean (defaults to <=).
        @param validation_func: A function that takes a value and returns a boolean (defaults to None).
        @param ordered: A boolean that indicates if the range is ordered (defaults to False). An ordered filter
                        will offer improved efficiency as once it gets outside of range it will throw a `STOP`.
        @param ignore_none: A boolean that indicates if None values should be ignored (defaults to False). If
                        set to True it will return `KEEP` if the value is None.
        """
        self.start = start
        self.end = end
        self.comparator = comparator or self.default_comparator
        self.validation_func = validation_func
        self.ordered = ordered
        self.ignore_none = ignore_none

    def default_comparator(self, a, b):
        return a < b

    def _validate(self, value):
        if self.validation_func:
            return self.validation_func(value)
        return True

    def check(self, value):
        # if end is 3 and value is 2 then self.comparator(end, value) -> 3 < 2
        if value is None:
            return FILTER_POSITION.KEEP if self.ignore_none else FILTER_POSITION.SKIP
        if not self._validate(value):
            return FILTER_POSITION.SKIP
        if self.comparator(value, self.start):
            return FILTER_POSITION.SKIP
        if self.comparator(self.end, value):
            return FILTER_POSITION.STOP if self.ordered else FILTER_POSITION.SKIP
        return FILTER_POSITION.KEEP
    
    def __str__(self):
        return f"RangeFilter(start={self.start}, end={self.end}, ordered={self.ordered}, ignore_none={self.ignore_none})"

    @classmethod
    def from_json(cls, json):
        return cls(json["start"], json["end"], json["ordered"], json["ignore_none"])

class DateFilter(RangeFilter):
    def __init__(self, start_date, end_date, ordered=False, ignore_timezone=False, ignore_none=False):
        """
        Process a datetime object and return KEEP either when the date
        is between the start and end date or when the date is None. Return
        SKIP when the date is before the start date and STOP when the date
        is after the end date.
        """
        self.ignore_timezone = ignore_timezone
        if not ignore_timezone and start_date.tzinfo is None:
            raise ValueError("Start date must be timezone aware")
        if not ignore_timezone and end_date.tzinfo is None:
            raise ValueError("End date must be timezone aware") 

        super().__init__(start_date, end_date, ordered=ordered, ignore_none=ignore_none)

    def check(self, value: datetime.datetime):
        if value and not self.ignore_timezone and value.tzinfo is None:
            raise ValueError("Value must be timezone aware")
        return super().check(value)

    def __str__(self):
        return f"DateFilter(start={self.start}, end={self.end}, ordered={self.ordered}, ignore_timezone={self.ignore_timezone}, ignore_none={self.ignore_none})"

    @classmethod
    def from_json(cls, json):
        return cls(datetime.datetime.fromtimestamp(json["start"], tz=datetime.UTC), datetime.datetime.fromtimestamp(json["end"], tz=datetime.UTC), json["ordered"], json["ignore_timezone"], json["ignore_none"])

class Filters:
    """
    A class to manage zero or more filters to be applied to a `PAMGuardFile` object.
    Apply a filter to a particular value by calling `filter()` method. Then check the
    `position` (type `FILTER_POSITION`) attribute to check the position of the filter.

    To see all available filters, see attribute `INSTALLED_FILTERS`. You can also add
    your own custom filters using the method `add_custom_filter()` and passing a 
    custom function. 
    """

    INSTALLED_FILTERS = {
        'uidlist': WhitelistFilter,
        'uidrange': RangeFilter,
        'daterange': DateFilter,
    }


    def __init__(self, filters: dict[str, BaseFilter] = None):
        """
        A class to manage zero or more filters to apply to a `PAMGuardFile` object.

        @param filters: A dictionary of filters to apply to a `PAMGuardFile` object.
                        The dictionary key is hte name of the filter (which is important
                        for in-built filters such as `uidlist`) and the value is the
                        filter object (extends `BaseFilter`). Defaults to `None`.
        """

        if not filters: filters = {}
        for key, value in filters.items():
            self.__validate(key, value)
        self.__filters: dict[str, BaseFilter] = filters
        self.position: FILTER_POSITION = None
        self.custom_filters = []
    
    def add_custom_filter(self, func: Callable[[any], bool]):
        """
        Add a custom filter function. The function should take a single argument
        (extends `BaseChunk`) and return a boolean (whether the filter succeeds).
        Custom filters are usually called just after an entire chunk has been read
        and determines if that chunk should be saved or not."""
        self.custom_filters.append(func)
    
    def call_custom_filters(self, chunk_obj):
        for func in self.custom_filters:
            res = func(chunk_obj)
            if res is not None and type(res) == FILTER_POSITION and res != FILTER_POSITION.KEEP:
                self.position = res
                raise FilterMismatchException()

    def add(self, key: str, value: BaseFilter):
        """
        Add a filter. `key` is the name of the filter (which is important
        for in-built filters such as `uidlist`) and the value is the
        filter object (extends `BaseFilter`).
        """
        self.__validate(key, value)
        self.__filters[key] = value
    
    def to_json(self):
        return {
            key: value.to_json() for key, value in self.__filters.items()
        }

    def __validate(self, key, value):
        if key in self.INSTALLED_FILTERS and not isinstance(value, self.INSTALLED_FILTERS[key]):
            raise ValueError(f"Filter {key} must be of type {self.INSTALLED_FILTERS[key]}")
        if key not in self.INSTALLED_FILTERS and not isinstance(value, BaseFilter):
            raise ValueError(f"Custom filter {key} must be of type FilterBinaryFile")

    def filter(self, key: str, value: any) -> None:
        """
        Pass a particular `value` into a filter of type `key`.
        Raises `FilterMismatchException` if the filter is not met

        @param key: The name of the filter to apply.
        @param value: The value to apply the filter to.
        """
        if key in self.__filters:
            self.position = self.__filters[key].check(value)
        else:
            self.position = FILTER_POSITION.KEEP
        
        if not self.position == FILTER_POSITION.KEEP:
            raise FilterMismatchException()

    # def __str__(self):
    #     if len(self.__filters) == 0:
    #         return "No filters"
    #     ret = f"Filters ({len(self.__filters)}):\n"
    #     for filter in self.__filters:
    #         ret += f"\t{filter}: {self.__filters[filter]}\n"
    #     return ret
    
    def __len__(self):
        return len(self.__filters)

    @property
    def filters(self):
        return self.__filters