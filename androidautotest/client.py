# -*- coding: UTF-8 -*-
import os
from .tool import PATHSEP
from .api import Device
from .errors import PathNotExistError,CaseNotFoundError

"""
androidautotest [-r|--run] <case_path> [-d|--device] <device_serial_number> [-t|--times] <run_times>',
case:case_path
device:device_serial_number
times:run_times
"""
# to execute case that is suffix with ".air"
EXECUTEABLE_FILE_SUFFIX = '.air'

def execute(case_path, device_serial_number, run_times):
    if not os.path.exists(case_path):
        raise PathNotExistError('path %s not exists' % case_path)
    
    if os.path.isfile(case_path):
        raise CaseNotFoundError('%s is a file, please choose case path(suffix with ".air"): ' % case_path)
    # single case
    elif case_path[-4:] == EXECUTEABLE_FILE_SUFFIX:
        for i in range(run_times):
            index_start = case_path.rfind(PATHSEP)
            case_name = case_path[index_start+1:-4]
            Device.switchDevice(device_serial_number)
            print('python %s%s%s.py' % (case_path, PATHSEP, case_name))
            os.system('python %s%s%s.py' % (case_path, PATHSEP, case_name))
    # case directory contains without case in it
    elif len(os.listdir(case_path)) == 0:
        raise CaseNotFoundError('there is no case in path %s' % case_path)
    else:
        dirs = os.listdir(case_path)
        case_dirs = []
        for dir in dirs:
            dir_path = case_path+PATHSEP+dir
            if os.path.isdir(dir_path) and dir_path[-4:] == EXECUTEABLE_FILE_SUFFIX:
                case_dirs.append(dir_path)
        if len(case_dirs) == 0:
            raise CaseNotFoundError('there is no case in path %s' % case_path)
        else:
            for i in range(run_times):
                for case_dir in case_dirs:
                    index_start = case_dir.rfind(PATHSEP)
                    case_name = case_dir[index_start+1:-4]
                    Device.switchDevice(device_serial_number)
                    print('python %s%s%s.py' % (case_dir, PATHSEP, case_name))
                    os.system('python %s%s%s.py' % (case_dir, PATHSEP, case_name))
