# -*- coding: UTF-8 -*-
import time
import os
import sys
import traceback
from enum import Enum
from androidautotest.tool import *
from androidautotest.logger import Logger

# auto install dependency
try:
	import psutil
except ModuleNotFoundError:
	os.system(r'python -m pip install --upgrade pip')
	os.system(r'pip install psutil -i https://pypi.tuna.tsinghua.edu.cn/simple/')
	import psutil
try:
	from PIL import Image
except ModuleNotFoundError:
	os.system(r'python -m pip install --upgrade pip')
	os.system(r'pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/')
	from PIL import Image
try:
	import numpy as np
except ModuleNotFoundError:
	os.system(r'python -m pip install --upgrade pip')
	os.system(r'pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/')
	import numpy as np
try:
	import cv2 as cv
except ModuleNotFoundError:
	os.system(r'python -m pip install --upgrade pip')
	os.system(r'pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple/')
	import cv2 as cv

'''
adb download: https://developer.android.google.cn/studio/releases/platform-tools.html
adb usage: https://juejin.im/post/5b5683bcf265da0f9b4dea96
match template: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html   
'''

# asm zoom size
class ASM:
	ZOOM_SIZE = 50

# case file name(like 'case001')
index_start = MODULE_PATH.rfind(PATHSEP)
case_name = MODULE_PATH[index_start+1:-4]

# template picture class
class Template:
	def __init__(self, name):
		self.name = name.replace('\\',PATHSEP)

	def getPath(self):
		return path_join(MODULE_PATH, self.name)

	def getName(self):
		return self.name

# logger
logger = Logger(case_name)

def path_join(*path):
	path_all = '' 
	for i in range(len(path)-1):
		path_all = path_all + path[i] + os.sep
	path_all = path_all + path[-1]
	return path_all

def assert_exists(template_pic, threshold=0.9, device='serial-number', timeout=10):
	logger.info(r"[androidtest] assert_exists('%s')" % template_pic.getName())
	
	start_time = time.time()
	end_time = time.time()
	while end_time-start_time < timeout:
		match_list = do_match(template_pic, threshold, device)
		if len(match_list) > 0:
			return
		else:
			end_time = time.time()
	try:
		raise RuntimeError(r'%s is not in screen' % (template_pic.getPath()))
	except RuntimeError as e:
		logger.error(r'[error] %s' % traceback.format_exc())

def assert_not_exists(template_pic, threshold=0.9, device='serial-number', timeout=10):
	logger.info(r"[androidtest] assert_not_exists('%s')" % template_pic.getName())
	
	start_time = time.time()
	end_time = time.time()
	while end_time-start_time < timeout:
		match_list = do_match(template_pic, threshold, device)
		if len(match_list) == 0:
			return
		else:
			end_time = time.time()
	try:
		raise RuntimeError(r'%s is in screen' % (template_pic.getPath()))
	except RuntimeError as e:
		logger.error(r'[error] %s' % traceback.format_exc())
	
def exists(template_pic, threshold=0.9, device='serial-number', timeout=10):
	logger.info(r"[androidtest] exists('%s')" % template_pic.getName())
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device
	
	start_time = time.time()
	end_time = time.time()
	while end_time-start_time < timeout:
		match_list = do_match(template_pic, threshold, device)
		if len(match_list) > 0:
			return True
		else:
			end_time = time.time()
	return False

def touch_point(point, device='serial-number'):
	logger.info(r"[androidtest] touch(%d, %d)" % (point[0],point[1]))
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device
	
	os.system(r'adb %s shell input tap %d %d' % (more,point[0],point[1]))
	logger.info(r'[adb] adb %s shell input tap %d %d' % (more,point[0],point[1]))

def touch(template_pic, threshold=0.9, device='serial-number', delay=0.4, timeout=10):
	# python is not support method override, use type judge 
	if type(template_pic) == list or type(template_pic) == tuple:
		touch_point(template_pic, device)
		return
	logger.info(r"[androidtest] touch('%s')" % template_pic.getName())
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device
	
	start_time = time.time()
	end_time = time.time()
	while end_time-start_time < timeout:
		match_list = do_match(template_pic, threshold, device)
		if len(match_list) > 0:
			point_x = (match_list[0][0]+match_list[0][2])*0.5
			point_y = (match_list[0][1]+match_list[0][3])*0.5
			if delay < 0.5:
				os.system(r'adb %s shell input tap %d %d' % (more,point_x,point_y))
				logger.info(r'[adb] adb %s shell input tap %d %d' % (more,point_x,point_y))
			else:
				os.system(r'adb %s shell input swipe %d %d %d %d %d' % (more,point_x,point_y,point_x,point_y,delay*1000))
				logger.info(r'[adb] adb %s shell input swipe %d %d %d %d %d' % (more,point_x,point_y,point_x,point_y,delay*1000))
			return
		else:
			end_time = time.time()
	try:
		raise RuntimeError(r'can not find %s in screen' % (template_pic.getPath()))
	except RuntimeError as e:
		logger.error(r'[error] %s' % traceback.format_exc())

def long_touch(template_pic, threshold=0.9, device='serial-number', delay=0.8, timeout=10):
	# python is not support method override, use type judge 
	if type(template_pic) == list or type(template_pic) == tuple:
		touch_point(template_pic, device)
		return
	logger.info(r"[androidtest] long_touch('%s')" % template_pic.getName())
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device
	
	start_time = time.time()
	end_time = time.time()
	while end_time-start_time < timeout:
		match_list = do_match(template_pic, threshold, device)
		if len(match_list) > 0:
			point_x = (match_list[0][0]+match_list[0][2])*0.5
			point_y = (match_list[0][1]+match_list[0][3])*0.5
			os.system(r'adb %s shell input swipe %d %d %d %d %d' % (more,point_x,point_y,point_x,point_y,delay*1000))
			logger.info(r'[adb] adb %s shell input swipe %d %d %d %d %d' % (more,point_x,point_y,point_x,point_y,delay*1000))
			return
		else:
			end_time = time.time()
	try:
		raise RuntimeError(r'can not find %s in screen' % (template_pic.getPath()))
	except RuntimeError as e:
		logger.error(r'[error] %s' % traceback.format_exc())

def touch_if(template_pic, threshold=0.9, device='serial-number', delay=0.4, timeout=10):
	logger.info(r"[androidtest] touch_if('%s')" % template_pic.getName())
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device
	
	start_time = time.time()
	end_time = time.time()
	while end_time-start_time < timeout:
		match_list = do_match(template_pic, threshold, device)
		if len(match_list) > 0:
			point_x = (match_list[0][0]+match_list[0][2])*0.5
			point_y = (match_list[0][1]+match_list[0][3])*0.5
			if delay < 0.5:
				os.system(r'adb %s shell input tap %d %d' % (more,point_x,point_y))
				logger.info(r'[adb] adb %s shell input tap %d %d' % (more,point_x,point_y))
			else:
				os.system(r'adb %s shell input swipe %d %d %d %d %d' % (more,point_x,point_y,point_x,point_y,delay*1000))
				logger.info(r'[adb] adb %s shell input swipe %d %d %d %d %d' % (more,point_x,point_y,point_x,point_y,delay*1000))
			return
		else:
			end_time = time.time()

def touch_in(template_pic, target_pic, threshold=0.9, device='serial-number', delay=0.4, timeout=10):
	logger.info(r"[androidtest] touch_in('%s', '%s')" % (template_pic.getName(), target_pic.getName()))
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device
	
	start_time = time.time()
	end_time = time.time()
	while end_time-start_time < timeout:
		target_match_list = do_match(target_pic, threshold, device)
		if len(target_match_list) > 0:
			target_point = target_match_list[0]
			template_match_list = do_match(template_pic, threshold, device)
			for pt in template_match_list:
				if pt[0] >= target_point[0] and pt[1] >= target_point[1] and pt[2] <= target_point[2] and pt[3] <= target_point[3]:
					logger.info('finded ractangle '+ str(pt) +' in ' + str(target_point))
					point_x = (pt[0]+pt[2])*0.5
					point_y = (pt[1]+pt[3])*0.5
					if delay < 0.5:
						os.system(r'adb %s shell input tap %d %d' % (more,point_x,point_y))
						logger.info(r'[adb] adb %s shell input tap %d %d' % (more,point_x,point_y))
					else:
						os.system(r'adb %s shell input swipe %d %d %d %d %d' % (more,point_x,point_y,point_x,point_y,delay*1000))
						logger.info(r'[adb] adb %s shell input swipe %d %d %d %d %d' % (more,point_x,point_y,point_x,point_y,delay*1000))
					return
			try:
				raise RuntimeError(r'can not find %s in %s' % (template_pic.getPath(), target_pic.getPath()))
			except RuntimeError as e:
				logger.error(r'[error] %s' % traceback.format_exc())
		else:
			end_time = time.time()
	try:
		raise RuntimeError(r'can not find %s in screen' % ( target_pic.getPath()))
	except RuntimeError as e:
		logger.error(r'[error] %s' % traceback.format_exc())

# return [(891, 1042, 1035, 1110), (891, 1650, 1035, 1718)] or [] ps:(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
def do_match(template_pic, threshold=0.9, device='serial-number'):
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device
	
	template_path = template_pic.getPath()
	# generate identify id 
	time_log, time_str, random_str = random_id()

	# adb shell screencap
	os.system(r'adb %s shell screencap -p /sdcard/sc.png' % more)
	logger.info(r'[adb] adb %s shell screencap -p /sdcard/sc.png' % more)
	
	# create picture name
	pic_name = r'screencap_%s%s.png' % (time_str, random_str)
	
	# adb shell push
	ADB_PULL = r'adb %s pull /sdcard/sc.png %s' % (more, logger.log_dir)
	os.system(ADB_PULL)
	logger.info('[adb] %s' % ADB_PULL)
	time.sleep(0.5)
	
	# save picture to log dir and delete sc.png
	screencap_path = path_join(logger.log_dir, pic_name)
	Image.open(path_join(logger.log_dir,'sc.png')).save(screencap_path, 'png')
	os.remove(path_join(logger.log_dir,'sc.png'))
	
	# do touchs
	logger.info('Trying finding: '+ template_path)
	match_list = template_match(screencap_path, template_path, threshold)
	if len(match_list) > 0:
		logger.info(r'[matching] {"template":"%s", "screencap":"%s", "exists":"%s", "confidence": "%f"}' % (template_path, screencap_path, r'True', match_list[0][4]))
	else:
		logger.info(r'[matching] {"template":"%s", "screencap":"%s", "exists":"%s",  "confidence": "0.0"}' % (template_path, screencap_path, r'False'))
	return match_list

def template_match(full_pic, template_pic, threshold):
	#print(r'ASM.ZOOM_SIZE:%d' % ASM.ZOOM_SIZE)
	img = cv.imread(full_pic,0)
	img2 = img.copy()
	template = cv.imread(template_pic,0)
	# use Android Screen Monitor to capture screen, zoom adjust to 50 precent
	# img.shape: output w,h
	# [::-1]: reverses the array
	w, h = template.shape[::-1]
	# zoom out template picture to 100 precent
	template2 = cv.resize(template, (int((w*100)/ASM.ZOOM_SIZE), int((h*100)/ASM.ZOOM_SIZE)), cv.INTER_LINEAR)
	w2, h2 = template2.shape[::-1]
	# Apply template Matching
	res = cv.matchTemplate(img, template2, cv.TM_CCOEFF_NORMED)
	# Store the coordinates of matched area in a numpy array 
	loc = np.where(res >= threshold)
	if loc[0].size == 0:
		return []
	# zip(*zipped): unpack tuples into lists.
	match_list = zip(*loc[::-1])
	res_list = []
	for pt in match_list: 
		if len(res_list) == 0:
			res_list.append((pt[0], pt[1], pt[0]+w2, pt[1]+h2, res[pt[1]][pt[0]]))
		elif pt[0] > res_list[-1][0]-5 and pt[0] < res_list[-1][0]+5 and pt[1] > res_list[-1][1]-5 and pt[1] < res_list[-1][1]+5:
			pass
		else:
			res_list.append((pt[0], pt[1], pt[0]+w2, pt[1]+h2))
	for res in res_list:
		logger.info(r'finded in ractangle:' + str(res))
	return res_list 

# direction enum
class Direction(Enum):
	DIR_UP = 'up'
	DIR_DOWN = 'down'
	DIR_LEFT = 'left'
	DIR_RIGHT = 'right'
# direction enum constant
DIR_UP = Direction.DIR_UP
DIR_DOWN = Direction.DIR_DOWN
DIR_LEFT = Direction.DIR_LEFT
DIR_RIGHT = Direction.DIR_RIGHT

def flick(start, direction, step=1, device='serial-number'):
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device
		
	logger.info(r'[androidtest] flick(%s, %s)' % (str(start), direction.name))
	
	r = os.popen(r'adb %s shell wm size' % more)
	# Physical size: 1080x1920
	lines = r.readlines()
	screen_size = lines[0][15:].strip(LINESEQ).split('x')
	w = int(screen_size[0])
	h = int(screen_size[1])

	if direction == DIR_UP:
		one_step_size = int(h*0.1)
		command = r'adb %s shell input swipe %d %d %d %d' % (more, start[0], start[1], start[0], start[0]-step * one_step_size)
		os.system(command)
		logger.info(r'[adb] adb %s shell input swipe %d %d %d %d' % (more, start[0], start[1], start[0], start[0]-step * one_step_size))
	elif direction == DIR_DOWN:
		one_step_size = int(h*0.1)
		command = r'adb %s shell input swipe %d %d %d %d' % (more, start[0], start[1], start[0], start[0]+step * one_step_size)
		logger.info(r'[adb] adb %s shell input swipe %d %d %d %d' % (more, start[0], start[1], start[0], start[0]+step * one_step_size))
		os.system(command)
	elif direction == DIR_LEFT:
		one_step_size = int(w*0.1)
		command = r'adb %s shell input swipe %d %d %d %d' % (more, start[0], start[1], start[0]-step * one_step_size, start[0])
		logger.info(r'[adb] adb %s shell input swipe %d %d %d %d' % (more, start[0], start[1], start[0]-step * one_step_size, start[0]))
		os.system(command)
	elif direction == DIR_RIGHT:
		one_step_size = int(w*0.1)
		command = r'adb %s shell input swipe %d %d %d %d' % (more, start[0], start[1], start[0]+step * one_step_size, start[0])
		logger.info(r'[adb] adb %s shell input swipe %d %d %d %d' % (more, start[0], start[1], start[0]+step * one_step_size, start[0]))
		os.system(command)
	else:
		try:
			raise RuntimeError(r'not support flick to %s' % direction)
		except RuntimeError as e:
			logger.error(r'[error] %s' % traceback.format_exc())

def swipe(start, end, device='serial-number'):
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device
		
	logger.info(r'[androidtest] swipe(%s, %s)' % (str(start), str(end)))
	command = r'adb %s shell input swipe %d %d %d %d' % (more, start[0], start[1], end[0], end[1])
	os.system(command)
	logger.info(r'[adb] adb %s shell input swipe %d %d %d %d' % (more, start[0], start[1], end[0], end[1]))

# keycode enum
class KeyCode(Enum):
	HOME = 3
	BACK = 4
	VOLUME_UP = 24
	VOLUME_DOWN = 25
	POWER = 26
# keycode enum constant
HOME = KeyCode.HOME
BACK = KeyCode.BACK
VOLUME_UP = KeyCode.VOLUME_UP
VOLUME_DOWN = KeyCode.VOLUME_DOWN
POWER = KeyCode.POWER

def keyevent(keycode, device='serial-number'):
	logger.info(r'[androidtest] keyevent(%s)' % keycode.name)
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device

	os.system(r'adb %s shell input keyevent %d' % (more, keycode.value))
	logger.info(r'[adb] adb %s shell input keyevent %d'% (more, keycode.value))

def text(input, device='serial-number'):
	logger.info(r"[androidtest] text('%s')" % input)
	# choose device by serial-number
	if device == 'serial-number':
		more = ''
	else:
		more = r'-s %s' % device

	os.system(r"adb %s shell input text '%s'" % (more, input))
	logger.info(r"[adb] adb %s shell input text '%s'" % (more, input))

def sleep(delay):
	logger.info(r'[androidtest] sleep(%s)' % str(delay))
	time.sleep(delay)
	
def end():
	logger.end()
