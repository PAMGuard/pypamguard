import glob
from pypamguard.load_pamguard_binary_file import load_pamguard_binary_file
from pypamguard.core.pamguardfile import PAMGuardFile
from pypamguard.core.filters import FILTER_POSITION
import os

def load_pamguard_binary_folder(directory: str, mask: str, files_ordered = True, clear_fields: list = []):
    result = {}
    for file in glob.glob(pathname=mask, root_dir=directory, recursive=True):
        res = load_pamguard_binary_file(os.path.join(directory,file))
        for field in clear_fields:
            setattr(res, field, None)
        if res.filters.position == FILTER_POSITION.STOP:
            if files_ordered: break
            else: continue
        result[file.replace(directory, "")] = res
       
    return result
