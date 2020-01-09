# -*- coding: UTF-8 -*-
import os
import time
import traceback
import random
import sys
import json
import webbrowser
import subprocess
import urllib.request
import platform
import zipfile
import shutil

# dirname:get parent directory
# sys.argv[0] getFileName
CASE_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
PATHSEP = os.sep
LINESEQ = os.linesep
PLATFORM = platform.system()
USER_HOME = os.path.expanduser('~')

def line_join(*str):
    str_all = '' 
    for i in range(len(str)):
        str_all = str_all + str[i]
    str_all = str_all + LINESEQ
    return str_all

def confidence_precent(value):
    return str(round(float(value)*100, 2))+'%'

def random_id():
    time_log = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    random_str = ''.join(random.sample(['0','1','2','3','4','5','6','7','8','9'], 6))
    return time_log, time_str, random_str

def open_new_tab(path):
    webbrowser.open_new_tab(path)

def set_adb_home():
    ADB_HOME = Path.path_join(USER_HOME, '.androidautotest', 'platform-tools')
    if PLATFORM  == 'Windows':
        Command.write('set path=%path%;{}'.format(ADB_HOME))
    elif PLATFORM == 'Linux':
        Command.write('export PATH={}:$PATH'.format(ADB_HOME))

class Path:
    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def isfile(path):
        return os.path.isfile(path)

    @staticmethod
    def listdir(path):
        return os.listdir(path)

    @staticmethod
    def isdir(path):
        return os.path.isdir(path)

    @staticmethod
    def remove(path):
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def makedirs(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def parent(path, isurl=False):
        if isurl:
            return path[0:path.rfind('/')]
        else:
            return path[0:path.rfind(PATHSEP)]

    @staticmethod
    def name(path, end=0, isurl=False):
        tmp = ''
        if isurl:
            tmp = path[path.rfind('/')+1:len(path)]
        else:
            tmp = path[path.rfind(PATHSEP)+1:len(path)]
            
        if end > 0:
            return tmp[0:end]
        elif end < 0:
            return tmp[0:len(tmp)+end]
        else:
            return tmp

    @staticmethod
    def copy(source, dest):
        shutil.copy(source, dest)

    @staticmethod
    def path_join(*path):
        path_all = '' 
        for i in range(len(path)-1):
            path_all = path_all + path[i] + PATHSEP
        path_all = path_all + path[-1]
        return path_all

class Command:
    @staticmethod
    def write(command):
        return os.system(command)

    @staticmethod
    def read(command):
        r = os.popen(command)
        # Physical size: 1080x1920
        lines = r.readlines()
        lines_no_lineseq = []
        for line in lines:
            line_no_lineseq = line.strip(LINESEQ)
            if line_no_lineseq != '':
                lines_no_lineseq.append(line.strip(LINESEQ))
        return lines_no_lineseq

    @staticmethod
    def exit(status=0):
        return sys.exit(status)

    @staticmethod
    def argv(position):
        return sys.argv[position]

    @staticmethod
    def traceback():
        return traceback.format_exc()

class Json:
    @staticmethod
    def dumps(obj):
        return json.dumps(obj)

    @staticmethod
    def loads(str):
        return json.loads(str, encoding="utf-8", strict=False)

class Timer:
    @staticmethod
    def time():
        return time.time()

    @staticmethod
    def sleep(sec):
        return time.sleep(sec)

    @staticmethod
    def strftime(format, time_value):
        return time.strftime(format, time.localtime(time_value))

    @staticmethod
    def calc(sec):
        sec = int(sec)
        second = 0
        minute = 0
        hour = 0
        if sec > 3600:
            hour = int(sec/3600)
            minute = int((sec - hour*3600)/60)
            second = sec - hour*3600 - minute*60
        elif sec > 60:
            hour = 0
            minute = int(sec/60)
            second = sec - hour*3600 - minute*60
        else:
            hour = 0
            minute = 0
            second = sec
        return hour, minute, second

class Downloader:
    __start_time = -1
    
    def download(self, http_url, dependency_dir):
        print('  Downloading %s ... ' % http_url)
        local_dir = Path.path_join(dependency_dir, Path.name(http_url, isurl=True))
        self.__start_time = time.time()
        urllib.request.urlretrieve(http_url, local_dir, self.__report_hook)
        print()
        # unzip file if file ends with 'zip'
        if Path.name(http_url, isurl=True).endswith('zip'):
            Ziper.unzip(local_dir, Path.parent(local_dir))

    def __report_hook(self, block_number, read_size, total_size):
        precent = int((100.0*block_number*read_size)/total_size)
        percent_str = '{}%'.format(precent)
        size, unit = self.__calc_byte(total_size)
        total_str = str(size) + unit
        
        size, unit = self.__calc_byte((block_number*read_size)/(time.time()-self.__start_time))
        time_left_str = '0:00:00'
        speed = (block_number*read_size)/(time.time()-self.__start_time)
        speed_str = '0kB/s'
        if speed != 0:
            speed_str = str(size) + unit +'/s'
            
            hour, minute, second = Timer.calc((total_size-block_number*read_size)/speed)
            time_left_str = str(hour).zfill(1) +':'+ str(minute).zfill(2) +':'+ str(second).zfill(2)
        
        if block_number*read_size < total_size:
            current_size_str = str(block_number*read_size) + '/' + str(total_size)
        else:
            current_size_str = str(total_size) + '/' + str(total_size)
        # \r to flush 
        sys.stdout.write('\r    %s |%s%s| %s %s [%s %s]' % (percent_str, '█' * int(precent/5), ' ' * int((100-precent)/5), total_str, current_size_str, time_left_str, speed_str))
        
        sys.stdout.flush()
        time.sleep(0.005)

    def __calc_byte(self, byte_size):
        size = 0
        unit = 'B'
        if byte_size < 102.4:#20B
            size = round(byte_size)
            unit = 'B'
        elif (byte_size/1024) < 1024:#
            size = round(byte_size/1024, 1)
            if size > 1:
                size = round(size)
            unit = 'kB'
        else:
            size = round(((byte_size/1024)/1024), 1)
            unit = 'MB'
        return size, unit

class Ziper:
    @staticmethod
    def unzip(zip_path, output_path):
        print('Unziping %s ... ' % zip_path)
        zip_file = zipfile.ZipFile(zip_path)
        for names in zip_file.namelist():  
            print('Extracting %s ...' % names)
            if not Path.exists(Path.path_join(output_path, names)):
                zip_file.extract(names, output_path)
        zip_file.close()
        Path.remove(zip_path)


