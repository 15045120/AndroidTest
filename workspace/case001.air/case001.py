# -*- coding: UTF-8 -*-
from androidautotest.api import *

# to home
keyevent(HOME)
keyevent(HOME,device='HMKNW17421063974')

# to FileBrowser
while not exists(Template(r'pic\20191215121636.png')):
	flick((400,400),DIR_LEFT,step=2)
touch(Template(r'pic\20191215121636.png'))
touch(Template(r'pic\20191215134814.png'))

# not in top screen of FileBrowser
if exists(Template(r'pic\20191215143440.png')):
	touch(Template(r'pic\20191215142057.png'))
	text('15045120')
else:
	touch([530,142])
	text('15045120')

# 15045120 is in screen
assert_exists(Template(r'pic\20191215142425.png'))

end()
