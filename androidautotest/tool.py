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
        

    
class Downloader:
    @staticmethod
    def download(http_url, dependency_dir):
        print('Downloading %s ... ' % http_url)
        local_dir = Path.path_join(dependency_dir, Path.name(http_url, isurl=True))
        urllib.request.urlretrieve(http_url, local_dir, Downloader.report_hook)
        print()
        # unzip file if file ends with 'zip'
        if Path.name(http_url, isurl=True).endswith('zip'):
            Ziper.unzip(local_dir, Path.parent(local_dir))
        
    @staticmethod
    def report_hook(block_number, head_size, total_size):
        precent = int((100.0*block_number*head_size)/total_size)
        percent_str = '{}%'.format(precent)
        # \r to flush 
        sys.stdout.write('\r[%s%s] %s' % ('#' * precent, '-' * (100-precent), percent_str))
        sys.stdout.flush()
        
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
