# -*- coding: UTF-8 -*-
import sys
import os
import re

# auto install dependency
print('start install dependency...')
os.system(r'python -m pip install --upgrade pip')
os.system(r'pip install psutil -i https://pypi.tuna.tsinghua.edu.cn/simple/')
os.system(r'pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/')
os.system(r'pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/')
os.system(r'pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple/')
print('install dependency successfully...')