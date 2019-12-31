# -*- coding: UTF-8 -*-
import os
import time
import traceback
import random
import sys
import json
import webbrowser

# dirname:get parent directory
# sys.argv[0] getFileName
CASE_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
PATHSEP = os.sep
LINESEQ = os.linesep

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
    def parent(path):
        return path[0:path.rfind(PATHSEP)]
        
    @staticmethod
    def name(path, end=-1):
        tmp = path[path.rfind(PATHSEP)+1:len(path)]
        return tmp[:end]
        
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
        return json.loads(str)
        
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