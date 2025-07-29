from pypamguard import load_pamguard_binary_file
from pypamguard.core.pamguardfile import PAMGuardFile
from pypamguard.chunks.base import BaseChunk
from pypamguard.utils.serializer import serialize
from pypamguard.core.filters import Filters, DateFilter, RangeFilter, WhitelistFilter, BaseFilter
from pypamguard.logger import Verbosity
import os, json
import pytest
from ._constants import TESTS

@pytest.fixture
def filters():
    return Filters()


def _compare_json(got_dict, expected_dict, test_name, chunk_name, path=""):
    if type(expected_dict) == dict:
        for attr, expected in expected_dict.items():
            if str(attr).startswith("_"): continue
            assert attr in got_dict, f"Test {test_name}: chunk '{chunk_name}' does not have attribute '{path}{attr}'"
            got = got_dict[attr]
            _compare_json(got, expected, test_name, chunk_name, path + f"{attr}.")
            # if type(expected) == dict:
            #     _compare_json(got, expected, test_name, chunk_name, path + f"{attr}.")
            # elif type(expected) == list:
            #     assert len(expected) == len(got)
            #     for i in range(len(expected) - 1):
            #         assert got[i] == expected[i]
            # else:
            #     if isinstance(got, float) and isinstance(expected, float):
            #         assert abs(got - expected) < 1e-6, f"Test {test_name}: chunk '{chunk_name}' attribute '{path}{attr}' has unexpected value: expected {expected} ({type(expected)}), got {got} ({type(got)})"
            #     else:
            #         assert got == expected, f"Test {test_name}: chunk '{chunk_name}' attribute '{path}{attr}' has unexpected value: expected {expected} ({type(expected)}), got {got} ({type(got)})"
    elif type(expected_dict) == list:
        assert len(expected_dict) == len(got_dict)
        for i in range(len(expected_dict) - 1):
            _compare_json(got_dict[i], expected_dict[i], test_name, chunk_name, path + f"[{i}]")
    else:
        if isinstance(got_dict, float) and isinstance(expected_dict, float):
            assert abs(got_dict - expected_dict) < 1e-6, f"Test {test_name}: chunk '{chunk_name}' attribute '{path}' has unexpected value: expected {expected_dict} ({type(expected_dict)}), got {got_dict} ({type(got_dict)})"
        else:
            assert got_dict == expected_dict, f"Test {test_name}: chunk '{chunk_name}' attribute '{path}' has unexpected value: expected {expected_dict} ({type(expected_dict)}), got {got_dict} ({type(got_dict)})"
            
def _test_chunk(chunk: BaseChunk, test_data: dict, test_name, chunk_name):
    if not chunk:
        assert test_data is None
        return
    _compare_json(chunk.to_json(), test_data, test_name, chunk_name)
  
def _get_paths(test_metadata):
    directory = os.path.join(test_metadata["directory"], test_metadata["filename"])
    json_path = os.path.join(test_metadata["directory"], test_metadata["json"])
    pgdf_path = f"{directory}.pgdf"
    pgdx_path = f"{directory}.pgdx"
    pgnf_path = f"{directory}.pgnf"
    assert os.path.exists(json_path)
    assert os.path.exists(pgdf_path)
    assert os.path.exists(pgdx_path)
    # assert os.path.exists(pgnf_path)
    return directory, json_path, pgdf_path, pgdx_path, pgnf_path

def _get_json_data(json_path):
    with open(json_path, "r") as f:
        json_data = json.loads(f.read())
        return json_data

def _run_header_tests(file: PAMGuardFile, json_data, test_name):
    assert "file_header" in json_data, "Test data is missing 'file_header'"
    assert "module_header" in json_data, "Test data is missing 'module_header'"
    _test_chunk(file.file_header, json_data["file_header"], test_name, "file_header")
    _test_chunk(file.module_header, json_data["module_header"], test_name, "module_header")

def _run_footer_tests(file: PAMGuardFile, json_data, test_name):
    assert "module_footer" in json_data, "Test data is missing 'module_footer'"
    assert "file_footer" in json_data, "Test data is missing 'file_footer'"
    _test_chunk(file.module_footer, json_data["module_footer"], test_name, "module_footer")
    _test_chunk(file.file_footer, json_data["file_footer"], test_name, "file_footer")

def _run_background_tests(file: PAMGuardFile, json_data, test_name):
    assert "background" in json_data, "Test data is missing 'background'"
    json_data_len = len(json_data["background"])
    assert len(file.background) == len(json_data["background"]), f"Test {test_name}: background length mismatch: expected {json_data_len}, got {len(file.background)}"
    for index, json_chunk in enumerate(json_data["background"]):
        _test_chunk(file.background[index], json_chunk, test_name, f"background[{index}]")

def _run_data_tests(file: PAMGuardFile, json_data, test_name):
    assert "data" in json_data, "Test data is missing 'data'"
    json_data_len = len(json_data["data"])
    assert len(file.data) == len(json_data["data"]), f"Test {test_name}: data length mismatch: expected {json_data_len}, got {len(file.data)}"
    for index, json_chunk in enumerate(json_data["data"]):
        _test_chunk(file.data[index], json_chunk, test_name, f"data[{index}]")

def _run_pgdf_tests(file: PAMGuardFile, json_data, test_name):
    _run_header_tests(file, json_data, test_name)
    _run_footer_tests(file, json_data, test_name)
    _run_data_tests(file, json_data, test_name)

def _run_pgdx_tests(file: PAMGuardFile, json_data, test_name):
    _run_header_tests(file, json_data, test_name)
    _run_footer_tests(file, json_data, test_name)
    assert file.data == [] or file.data == None, f"Test {test_name}: data should be empty"

def _run_pgnf_tests(file: PAMGuardFile, json_data, test_name):
    _run_header_tests(file, json_data, test_name)
    _run_footer_tests(file, json_data, test_name)
    _run_background_tests(file, json_data, test_name)

def get_filters(test_data, filters):
    filters_json = test_data["filters"]
    if filters_json:
        for filter in filters_json:
            filters.add(filter, BaseFilter.from_json(filters_json[filter]))
    return filters

@pytest.mark.parametrize("test_data", TESTS, ids=[os.path.join(x["directory"], x["json"]) for x in TESTS])
def test_module(test_data, filters):    
    directory, json_path, pgdf_path, pgdx_path, pgnf_path = _get_paths(test_data)
    json_data = _get_json_data(json_path)
    get_filters(json_data, filters)

    if "background" in test_data and test_data["background"]:
        file_pgnf = load_pamguard_binary_file(pgnf_path, verbosity=Verbosity.WARNING, filters=filters)   
        assert isinstance(file_pgnf, PAMGuardFile)
        _run_pgnf_tests(file_pgnf, json_data, json_path + " (PGNF)")
    else :
        file_pgdf = load_pamguard_binary_file(pgdf_path, verbosity=Verbosity.WARNING, filters=filters)   
        assert isinstance(file_pgdf, PAMGuardFile)
        _run_pgdf_tests(file_pgdf, json_data, json_path + " (PGDF)")
        file_pgdx = load_pamguard_binary_file(pgdx_path, verbosity=Verbosity.WARNING, filters=filters)
        # TODO: activate PGDX tests
        # _run_pgdx_tests(file_pgdx, json_data, json_path + " (PGDX)")


    # pgdx_file = load_pamguard_binary_file(pgdx_file, verbosity=Verbosity.WARNING, filters=filters)
    # _run_pgdx_tests(pgdx_file, json_data, json_path)