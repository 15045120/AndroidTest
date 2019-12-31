
# AndroidTest

The package is for android auto test, based on Python enviroment.

Basic thought is using ADB (Android Debug Bridge) to send command to Android test Phone connected with the PC and match picture by match template algorithm in opencv-python.
## Requirement
 1. ADB ([Android Debug Bridge](https://github.com/15045120/AndroidTest/tree/master/dependency/adb))
Follow information indicate you have installed ADB successfully.
    ```bash
    > adb
    Android Debug Bridge version 1.0.41
    Version 29.0.5-5949299
    Installed as E:\AndroidTest\dependency\adb\adb.exe
    ...
    ```
    
 2. ASM ([Android Screen Monitor](https://github.com/15045120/AndroidTest/blob/master/dependency/asm.jar))
 Use to capture partial picture, and you need to install JDK in your computer before running it.

     - Simple to use:
    ```bash
    java -jar asm.jar
    ```
     - Then adjust zoom to 50%, you can also set zoom to other size, but need to add some code in your case source file after your create your case file:
    ```python
    # adjust asm zoom to other size, 25% 
    ASM.ZOOM_SIZE = 25
    ```
## Installation
 
 1.Install androidautotest
```bash
pip install androidautotest 
```
Follow information indicate you have installed androidautotest successfully.
```bash
> python -m androidautotest
usage: androidautotest [--casedir CASEDIR] [--device DEVICE] [--times TIMES] [--newcase NEWCASE] [--savedir SAVEDIR]

A framework to run test case for android automated test

optional arguments:
  -V, --version      Print version and exit
  -h, --help         Print this help message and exit

create options:
  --newcase NEWCASE  New case name to create
  --savedir SAVEDIR  Path to save new case

run options:
  --casedir CASEDIR  Case path to run
  --device DEVICE    Device to switch
  --times TIMES      Times of case running
```
 2.create a new case to start your test task with Android Phone(For example: to create a new case named 'case001').

```bash
python -m androidautotest --newcase case001 --savedir E:\AndroidTest\workspace
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
Once you finish your code writing, you can run your case.

For example, run case001 with Android Phone which's serial number is 'HMKNW17421063974' for 10 times, you can write as follow.
```bash
python -m androidautotest --casedir E:\AndroidTest\workspace\case001.air --device HMKNW17421063974 --times 10
```
And there are three log files you can use to analyze your test plan after run your case.

In case001.air\log\case001.log.20191222010717_540637\:
 - log_case001_XXX.txt:all log output
 - serial_log_case001_XXX.txt:adb log output
 - adb log output:report of case run

