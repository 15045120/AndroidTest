# AndroidTest

The package is for android auto test, based on Python enviroment.

Basic thought is using ADB (Android Debug Bridge) to send command to Android test Phone connected with the PC and match picture by match template algorithm in opencv-python.

## Installation
 1.Install ADB ([Android Debug Bridge](https://github.com/15045120/AndroidTest/tree/master/dependency/adb)), and add it to path.
 
 2.Use ASM ([Android Screen Monitor](https://github.com/15045120/AndroidTest/blob/master/dependency/asm.jar)) to capture partial picture, and you need to install JDK in your computer first to run it.

 - Simple to use:
```bash
java -jar asm.jar
```
 - Then adjust zoom to 50%, you also can set to other size, but need to add some code in your case source file after your create your case file:
```python
# if adjust asm zoom to 25% 
ASM.ZOOM_SIZE = 25
```
3.Install androidautotest
```bash
pip install androidautotest 
```
4.If you cannot install dependency of androidautotest using 'pip install androidautotest', you can use [tools\install.py](https://github.com/15045120/AndroidTest/blob/master/tools/install.py)
```bash
python install.py
```
 5.Use [tools\newCase.py](https://github.com/15045120/AndroidTest/blob/master/tools/newCase.py) to create a new case to start your test task with Android Phone.

```bash
python newCase.py <caseName> <savePath>
```
## Documentation
You can find the complete AndroidTest API documentation on  [readthedocs](http://androidtest.readthedocs.io/).
## Examples
```python
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
```
Once you finish your code writing, you can run your case(for example: you create a case named 'case001'):
```bash
python -m androidautotest -h

usage: androidautotest [-r|--run] <case_path> [-d|--device] <device_serial_number> [-t|--times] <run_times>

A framework to run test case

optional arguments:
  -V, --version         Print version and exit
  -h, --help            Print this help message and exit

cmdlines options:
  -c <case_path>, --case <case_path>
                        Case path to run
  -d <device_serial_number>, --device <device_serial_number>
                        Device to switch
  -t <run_times>, --times <run_times>
                        Times of case running
```
For example, run case001 with Android Phone which's serial number is 'HMKNW17421063974' for 10 times, you can write as follow.
```bash
python -m androidautotest --case=E:\AndroidTest\workspace\case001.air --device=HMKNW17421063974 --times=10
```
And there are three log files you can use to analyze your test plan after run your case.

In case001.air\log\case001.log.20191222010717_540637\:
 - log_case001_XXX.txt:all log output
 - serial_log_case001_XXX.txt:adb log output
 - adb log output:report of case run