# -*- coding: UTF-8 -*-
from .tool import PATHSEP,Path,Command
from .errors import PathNotExistError,CaseNotFoundError
from .logger import SummaryLogger
"""
androidautotest [--casedir CASEDIR] [--device DEVICE] [--times TIMES],
casedir:case_path
device:device_serial_number
times:run_times
"""
# to execute case that is suffix with ".air"
EXECUTEABLE_FILE_SUFFIX = '.air'

def execute(case_path, device_serial_number, run_times):
    if not Path.exists(case_path):
        raise PathNotExistError('path %s not exists' % case_path)
    
    if Path.isfile(case_path):
        raise CaseNotFoundError('%s is a file, please choose case path(suffix with ".air"): ' % case_path)
    # single case
    elif case_path[-4:] == EXECUTEABLE_FILE_SUFFIX:
        # switch device
        from .api import Device 
        Device.switchDevice(device_serial_number)
        # generate summary id
        case_dir = Path.parent(case_path)
        SummaryLogger.start(case_dir)
        # run case
        for i in range(run_times):
            case_name = Path.name(case_path, -4)
            print('python %s%s%s.py' % (case_path, PATHSEP, case_name))
            Command.write('python %s%s%s.py' % (case_path, PATHSEP, case_name))
        SummaryLogger.end(case_dir)
    # case directory contains without case in it
    elif len(Path.listdir(case_path)) == 0:
        raise CaseNotFoundError('there is no case in path %s' % case_path)
    else:
        dirs = Path.listdir(case_path)
        case_dirs = []
        for dir in dirs:
            dir_path = case_path+PATHSEP+dir
            if Path.isdir(dir_path) and dir_path[-4:] == EXECUTEABLE_FILE_SUFFIX:
                case_dirs.append(dir_path)
        if len(case_dirs) == 0:
            raise CaseNotFoundError('there is no case in path %s' % case_path)
        else:
            # switch device
            from .api import Device 
            Device.switchDevice(device_serial_number)
            # generate summary id
            all_case_dir = case_path
            SummaryLogger.start(all_case_dir)
            # run case
            for i in range(run_times):
                for case_dir in case_dirs:
                    case_name = Path.name(case_dir, -4)
                    print('python %s%s%s.py' % (case_dir, PATHSEP, case_name))
                    Command.write('python %s%s%s.py' % (case_dir, PATHSEP, case_name))
            SummaryLogger.end(all_case_dir)
