# -*- coding: UTF-8 -*-
import sys
import os

if len(sys.argv) != 3:
	print(r'usage: python newCase.py <caseName> <savePath>')
else:
	print(r'create case %s start...' % sys.argv[1])
	case_name = sys.argv[1]
	module_path = os.path.abspath('.')
	# <caseName>.air
	case_dir = r'%s\%s.air' % (sys.argv[2], case_name)
	
	# <caseName>.air\log
	case_log_dir = r'%s\%s.air\log' % (sys.argv[2], case_name)
	
	# <caseName>.air\pic
	case_pic_dir = r'%s\%s.air\pic' % (sys.argv[2], case_name)
	if not os.path.exists(case_dir):
		os.makedirs(case_log_dir)
		os.makedirs(case_pic_dir)
		# <caseName>.air\<caseName.py>
		case_file_path = r'%s\%s.air\%s.py' % (sys.argv[2], case_name, case_name)
		case_file = open(case_file_path, mode='w')
		case_file.write('# -*- coding: UTF-8 -*-\n')
		case_file.write('from androidautotest.api import *\n')
		case_file.write('# Enter your code here\n')
		case_file.write('\n')
		case_file.write('\n')
		case_file.write('\n')
		case_file.write('end()')
		case_file.close()
		print(r'case %s has saved to path %s succfully...' % (sys.argv[1],sys.argv[2]))
	else:
		print(r'case %s has exist in path %s' % (sys.argv[1],sys.argv[2]))
