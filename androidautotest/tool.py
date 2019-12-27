# -*- coding: UTF-8 -*-
import os
import time
import random

MODULE_PATH = os.path.abspath('.')
PATHSEP = os.sep
LINESEQ = os.linesep

def path_join(*path):
    path_all = '' 
    for i in range(len(path)-1):
        path_all = path_all + path[i] + PATHSEP
    path_all = path_all + path[-1]
    return path_all

def line_join(*str):
    str_all = '' 
    for i in range(len(str)):
        str_all = str_all + str[i]
    str_all = str_all + LINESEQ
    return str_all

def random_id():
    time_log = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    random_str = ''.join(random.sample(['0','1','2','3','4','5','6','7','8','9'], 6))
    return time_log, time_str, random_str
    
def read_lines(cmd):
    r = os.popen(cmd)
    # Physical size: 1080x1920
    lines = r.readlines()
    lines_no_lineseq = []
    for line in lines:
        line_no_lineseq = line.strip(LINESEQ)
        if line_no_lineseq != '':
            lines_no_lineseq.append(line.strip(LINESEQ))
    return lines_no_lineseq
    
def confidence_precent(value):
    return str(round(float(value)*100, 2))+'%'