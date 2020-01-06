
# AndroidTest

The package is for android auto test, based on Python enviroment.

Basic thought is using ADB (Android Debug Bridge) to send command to Android test Phone connected with the PC and match picture by match template algorithm in opencv-python.
## Requirement
 1.ADB ([Android Debug Bridge](https://github.com/15045120/AndroidTest/tree/master/dependency/adb))


2.ASM ([Android Screen Monitor](https://github.com/15045120/AndroidTest/blob/master/dependency/asm.jar))

 Use to capture partial picture, and you need to install JDK in your computer before running it.

 Then adjust zoom to 50%, you can also set zoom to other size, but need to add some code in your case source file after your create your case file:
```python
# adjust asm zoom to other size, 25% 
ASM.ZOOM_SIZE = 25
```

3.Tesseract ([Tesseract-OCR](https://github.com/tesseract-ocr/tesseract))

 If you want to use the mechod 'image_to_string' in the 'androidautotest.api' which can recognize text in pictures, you need to install Tesseract and install testdata necessary like chinese 'chi_sim'.

## Installation & Usage

 1.Install androidautotest
```bash
pip install androidautotest 
```
Follow information indicate you have installed androidautotest successfully.
```bash
> python -m androidautotest
usage:
  androidautotest --installdep
  androidautotest --startasm
  androidautotest --newcase <NEWCASE> --savedir <SAVEDIR>
  androidautotest --casedir <CASEDIR> --device <DEVICE> --times <TIMES>

A framework to run test case for android automated test

optional arguments:
  -V, --version        Print version and exit
  -h, --help           Print this help message and exit

install dependency:
  --installdep         install dependency of androidautotest

start asm:
  --startasm           start Android Screen Monitor

create case:
  --newcase <NEWCASE>  New case name to create
  --savedir <SAVEDIR>  Path to save new case

run case:
  --casedir <CASEDIR>  Case path to run
  --device <DEVICE>    Device to switch
  --times <TIMES>      Times of case running
```
 2.install requirements 

```bash
python -m androidautotest --installdep
```
 3.start Android Screen Monitor(First, connect your Android Phone with PC, and open adb debug mode), then run follow command:

```bash
python -m androidautotest --startasm
```
 4.create a new case to start your test task with Android Phone(For example: to create a new case named 'case001').

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

For example, run case001 with Android Phone which's serial number is 'HMKNW17421063974' for 5 times, you can write as follow.
```bash
python -m androidautotest --casedir E:\AndroidTest\workspace\case001.air --device HMKNW17421063974 --times 5
```
And there are three log files you can use to analyze your test plan after run your case.

In case001.air\log\case001.log.20191222010717_540637:

1.log_case001_XXX.txt: all log output

2.serial_log_case001_XXX.txt: adb log output

3.adb log output: report of case run