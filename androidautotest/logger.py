# -*- coding: UTF-8 -*-
import os
import sys
import json
import webbrowser
from androidautotest.tool import *

# logger class
class Logger:
	log_dir = ''
	case_name = ''
	log_file_path = ''
	html_file_path = ''
	serial_file_path = ''
	start_time = ''
	
	log_list = []
	def __init__(self, case_name):
		self.case_name = case_name 
		# generate log file name
		time_log, time_str, random_str = random_id()
		# create log dir
		log_dir = r'%s%s%s.log.%s_%s' % (MODULE_PATH, PATHSEP, case_name, time_str, random_str)
		if not os.path.exists(log_dir):
			os.makedirs(log_dir)
		self.log_dir = log_dir
		self.log_file_path = r'%s%slog_%s_%s_%s.txt' % (log_dir, PATHSEP, case_name, time_str, random_str)
		self.html_file_path = r'%s%sreport_%s_%s_%s.html' % (log_dir, PATHSEP, case_name, time_str, random_str)
		self.serial_file_path = r'%s%sserial_log_%s_%s_%s.txt' % (log_dir, PATHSEP, case_name, time_str, random_str)
		print(r'------------------------------------------------------------')
		print(r'case %s start...' % self.case_name)
		self.start_time = time.time()

	def info(self, msg):
		log_file = open(self.log_file_path, mode='a+')
		print(msg)
		time_log, time_str, random_str = random_id()
		log_file.write(line_join(time_log, msg))
		log_file.close()
		if msg.startswith('[androidtest]') or msg.startswith('[matching]'):
			self.log_list.append(line_join(time_log, msg))
		elif msg.startswith('[adb]'):
			serial_file = open(self.serial_file_path, mode='a+')
			serial_file.write(line_join(time_log, msg))
			serial_file.close()

	def error(self, msg):
		log_file = open(self.log_file_path, mode='a+')
		print(msg)
		time_log, time_str, random_str = random_id()
		log_file.write(line_join(time_log, msg))
		log_file.close()
		self.log_list.append(line_join(time_log, msg))
		self.end(status='error')
	
	def end(self, status='normal'):
		log_list = self.log_list
		# time consuming
		consuming_time = time.time() - self.start_time
		html_file = open(self.html_file_path, mode='a+')
		html_file.write('<meta http-equiv="Content-Type" content="text/html;charset=utf-8">')
		html_file.write('<body style="width:80%;margin-left:10%;">')
		if status == 'normal':
			html_file.write(r'<div id="top" style="background: #ffffff;padding-left:20px;box-shadow: 0px 0px 10px #888888;border-radius:5px;height:80px;font-size:20px;">')
			html_file.write(r'<p>Test Case %s: <span style="color:green;font-weight:blod;">Pass</span></p>' % self.case_name)
			html_file.write(r'<p>Time consuming: <span style="color:red;">%ds</span><p></div>' % consuming_time)
			html_file.write(r'</div>')
		else:
			html_file.write(r'<div id="top" style="background: #ffffff;padding-left:20px;box-shadow: 0px 0px 10px #888888;border-radius:5px;height:80px;font-size:20px;">')
			html_file.write(r'<p>Test Case %s: <span style="color:red;font-weight:blod;">Fail</span></p>' % self.case_name)
			html_file.write(r'<p>Time consuming: <span style="color:red;">%ds</span><p></div>' % consuming_time)
			html_file.write(r'</div>')
		steps = []
		count = 0
		for i, log in enumerate(log_list):
			html_file.write('<div>')
			if log.find(r'[androidtest]') != -1:
				count = count + 1
				html_file.write('<div id="step%d" style="background: #6ab0de;box-shadow: 0px 0px 5px #888888; margin-top:20px;color:#ffffff;height:40px;line-height:40px;font-size:18px;padding-left:20px;">[Step%d] %s</div>' % (count, count, log.replace(r'[androidtest]', '')))
				steps.append({'step':count,'status':'success'})
			elif log.find(r'[matching]') != -1:
				if (i < len(log_list)-1 and log_list[i+1].find(r'[androidtest]') != -1) or i == len(log_list)-1:
					matchObj = {}
					# window
					if PATHSEP == '\\':
						matchObj = json.loads(log[33:].replace('\\', r'\\'))
					else:# linux
						matchObj = json.loads(log[33:])
					html_file.write('<div style="box-shadow: 0px 0px 5px #888888;">')
					html_file.write('<div style="padding-left:20px;font-weight:blod;">Target:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="%s"></img></div>' % matchObj['template'])
					html_file.write('<div style="margin-top:10px;padding-left:20px;font-weight:blod;">Screencap: <img src="%s"></img></div>' % matchObj['screencap'])
					if matchObj['exists'] == 'True':
						html_file.write('<div style="margin-top:10px;padding-left:20px;font-weight:blod;">Confidence: %s</div>' % confidence_precent(matchObj['confidence']))
						html_file.write('<div style="background: #e7f2fa;height:40px;line-height:40px;padding-left:20px;margin-top:10px;font-weight:blod;">Target picture is in screen</div>')
					else:
						html_file.write('<div style="background: #e7f2fa;height:40px;line-height:40px;padding-left:20px;margin-top:10px;font-weight:blod;">Target picture is not in screen</div>')
					html_file.write('</div>')
			elif log.find(r'[error]') != -1:
				steps[-1]['status'] = 'error'
				print(log[30:])
				html_file.write('<div style="background: #eeffcc;box-shadow: 0px 0px 5px #888888; height:200px;padding-left:20px;"><pre>%s</pre></div>' % log[30:])
			html_file.write('</div>')
		# navigation
		html_file.write('<div style="position:fixed;display: flex;flex-direction: row;bottom:20px;z-index:10000;right:10px;background:#e9ecef;border-radius:5px;padding:10px;">')
		for step_obj in steps:
			if step_obj['status'] == 'success':
				html_file.write('<a href="#step%d" style="background: #6ab0de;color:#ffffff;margin-right:10px;border-radius:20px;height:40px;width:40px;line-height:40px;text-align:center;text-decoration:none;color:#ffffff;">%d</a>' % (step_obj['step'],step_obj['step']))
			else:
				html_file.write('<a href="#step%d" style="background: red;color:#ffffff;margin-right:10px;border-radius:20px;height:40px;width:40px;line-height:40px;text-align:center;text-decoration:none;color:#ffffff;">%d</a>' % (step_obj['step'],step_obj['step']))
		html_file.write('<a href="#top" style="background: #6ab0de;color:#ffffff;margin-right:10px;border-radius:20px;height:40px;width:40px;line-height:40px;text-align:center;text-decoration:none;color:#ffffff;">Top</a>')
		html_file.write('</div>')
		html_file.write('</body>')
		html_file.write('</html>')
		html_file.close()
		print(r'case %s end...' % self.case_name)
		print(r'------------------------------------------------------------')
		# open browser
		webbrowser.open_new_tab(self.html_file_path)
		sys.exit(0)