# -*- coding: UTF-8 -*-
from .tool import PATHSEP,LINESEQ,PLATFORM,USER_HOME,Path,Command,Downloader
from .errors import PathNotExistError,CaseNotFoundError,CaseHasExistError,ADBNotFoundError,JavaNotFoundError,NoDeviceError
from .logger import SummaryLogger

# to execute case that is suffix with ".air"
EXECUTEABLE_FILE_SUFFIX = '.air'

# run case
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

# create new case
def create(new_case_name, save_dir):
    if not Path.exists(save_dir):
        raise PathNotExistError('case save path %s not exists' % save_dir)
    if Path.exists('%s%s%s.air' % (save_dir, PATHSEP, new_case_name)):
        raise CaseHasExistError('case %s has exist in path %s' % (new_case_name, save_dir))
        
    print(r'create case %s start...' % new_case_name)
    print(r'------------------------------------------------------------')
    
    # <savedir>\<newcase>.air
    case_dir = r'%s%s%s.air' % (save_dir, PATHSEP, new_case_name)
    Path.makedirs(case_dir)
    print('create %s' % case_dir)
    # <savedir>\<newcase>.air\log
    case_log_dir = r'%s%s%s.air%slog' % (save_dir, PATHSEP, new_case_name, PATHSEP)
    Path.makedirs(case_log_dir)
    print('create %s' % case_log_dir)
    # <savedir>\<newcase>.air\pic
    case_pic_dir = r'%s%s%s.air%spic' % (save_dir, PATHSEP, new_case_name, PATHSEP)
    Path.makedirs(case_pic_dir)
    print('create %s' % case_pic_dir)
    # <savedir>\<newcase>.air\<newcase.py>
    case_file_path = r'%s%s%s.air%s%s.py' % (save_dir, PATHSEP, new_case_name, PATHSEP, new_case_name)
    case_file = open(case_file_path, mode='w')
    case_file.write(r'# -*- coding: UTF-8 -*-%s' % LINESEQ)
    case_file.write(r'from androidautotest.api import *%s' % LINESEQ)
    case_file.write(r'# Enter your code here%s' % LINESEQ)
    case_file.write(LINESEQ)
    case_file.write(LINESEQ)
    case_file.write(LINESEQ)
    case_file.write('end()')
    case_file.close()
    print('create %s' % case_file_path)
    print(r'------------------------------------------------------------')
    print(r'case %s has saved to path %s succfully...' % (new_case_name, save_dir))

# install dependency
def install():
    # ~/.androidautotest
    module_path = Path.path_join(USER_HOME, '.androidautotest')
    Path.makedirs(module_path)

    # install adb
    print('Install ADB(Android Debug Bridge) ...')
    if PLATFORM  == 'Windows':
        Downloader().download('https://dl.google.com/android/repository/platform-tools-latest-windows.zip', module_path)
        msg = 'To use androidautotest, do the following: \n \
    add {} to Path'.format(Path.path_join(module_path, 'platform-tools'))
        
    elif PLATFORM == 'Linux':
        Downloader().download('https://dl.google.com/android/repository/platform-tools_r29.0.5-linux.zip', module_path)
        msg = '  To use androidautotest, do the following: \n \
    1.edit file named .bashrc \n \
    sudo vi ~/.bashrc \n \
    2.add follow code in the end of the file \n \
    export PATH=$PATH:{} \n \
    3.valid the environment variable \n \
    source ~/.bashrc'.format(Path.path_join(module_path, 'platform-tools'))
    
    print('Install ADB(Android Debug Bridge) Successfully')
    
    # install asm
    print('Install ASM(Android Screen Monitor) ...')
    Downloader().download('http://lc-4z6WybNb.cn-n1.lcfile.com/7935d55ddfbc6360797f/asm4androidautotest.zip', module_path)
    print('Install ASM(Android Screen Monitor) Successfully')
    
    # copy asm.jar file to platform-tools directory
    Path.copy(Path.path_join(module_path, 'asm.jar'), Path.path_join(module_path, 'platform-tools'))

    # remove asm.jar
    Path.remove(Path.path_join(module_path, 'asm.jar'))

    # to valid escape character
    Command.write("")
    print('\033[31m{}\033[0m'.format(msg))

# start asm
def startasm():
    lines = Command.read(r'adb')
    if len(lines) == 0:
        raise ADBNotFoundError()
        
    lines = Command.read(r'adb devices')
    # 'List of devices attached'
    if len(lines) == 1:
        raise NoDeviceError(r'there is no android device connect with PC')
        
    # ~/.androidautotest
    module_path = Path.path_join(USER_HOME, '.androidautotest')
    Command.write('java -jar %s' % Path.path_join(module_path, 'platform-tools', 'asm.jar'))
