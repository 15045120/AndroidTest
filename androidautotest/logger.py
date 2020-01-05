# -*- coding: UTF-8 -*-
from .tool import *

class SummaryLogger:
    @staticmethod
    def write(log):
        case_dir = log['dir']
        summary_log_path = '%s%ssummary_report.html' % (case_dir, PATHSEP)
        with open(summary_log_path, mode='a', encoding='utf-8') as html_file:
            #{"time":Timer.strftime("%Y%m%d%H%M%S", self.start_time),"name":self.case_name,"dir":case_dir, "url":self.html_file_path,"status":status}
            html_file.write('<tr>')
            html_file.write('<td>%s</td>' % log['name'])
            html_file.write('<td>%s</td>' % log['path'])
            html_file.write('<td>%s</td>' % log['time'])
            if log['status'] == 'pass':
                html_file.write('<td><a href="%s" style="color:green;">PASS</a></td>' % (log['url']))
            else:
                html_file.write('<td><a href="%s" style="color:red;">FAIL</a></td>' % (log['url']))
            html_file.write('<tr>')

    @staticmethod
    def start(case_dir):
        summary_log_path = '%s%ssummary_report.html' % (case_dir, PATHSEP)
        Path.remove(summary_log_path)
        with open(summary_log_path, mode='a', encoding='utf-8') as html_file:
            html_file.write('<meta http-equiv="Content-Type" content="text/html;charset=utf-8">')
            html_file.write('<body style="width:80%;margin-left:10%;">')
            html_file.write(r'<div id="top" style="background: #ffffff;padding-left:20px;box-shadow: 0px 0px 10px #888888;border-radius:5px;height:60px;line-height:60px;font-size:20px;text-align:center;">')
            html_file.write(r'<p>Test Case Summary report</p>')
            html_file.write(r'</div>')
            html_file.write('<table style="width:100%;margin-top:20px;" border="1" cellspacing="0">')
            html_file.write('<tr><th>case</th><th>directory</th><th>time</th><th>result</th></tr>')

    @staticmethod
    def end(case_dir):
        summary_log_path = '%s%ssummary_report.html' % (case_dir, PATHSEP)
        with open(summary_log_path, mode='a', encoding='utf-8') as html_file:
            html_file.write('</table></body></html>')
        open_new_tab(summary_log_path)
        
# logger class
class Logger:
    log_dir = ''
    case_name = ''
    log_file_path = ''
    html_file_path = ''
    serial_file_path = ''
    start_time = ''
    is_start = False
    log_info_list = []
    
    def __init__(self):
        # case file name(like 'case001')
        case_name = Path.name(CASE_PATH, -4)
        # open log when output first message
        self.is_start = False
        self.case_name = case_name 
        # generate log file name
        time_log, time_str, random_str = random_id()
        # create log dir
        log_dir = r'%s%slog%s%s.log.%s_%s' % (CASE_PATH, PATHSEP, PATHSEP, case_name, time_str, random_str)
        Path.makedirs(log_dir)
        self.log_dir = log_dir
        self.log_file_path = r'%s%slog_%s_%s_%s.txt' % (log_dir, PATHSEP, case_name, time_str, random_str)
        self.html_file_path = r'%s%sreport_%s_%s_%s.html' % (log_dir, PATHSEP, case_name, time_str, random_str)
        self.serial_file_path = r'%s%sserial_log_%s_%s_%s.txt' % (log_dir, PATHSEP, case_name, time_str, random_str)

    def start(self):
        print(r'------------------------------------------------------------')
        print(r'case %s start...' % self.case_name)
        
        self.start_time = Timer.time()
        self.is_start = True

    def info(self, msg):
        # start log if first time
        if not self.is_start:
            self.start()
        log_file = open(self.log_file_path, mode='a+', encoding='utf-8')
        print(msg)
        time_log, time_str, random_str = random_id()
        log_file.write(line_join(time_log, msg))
        log_file.close()
        if msg.startswith('[androidtest]') or msg.startswith('[matching]') or  msg.startswith('[tesseract]'):
            self.log_info_list.append(line_join(time_log, msg))
        elif msg.startswith('[adb]'):
            serial_file = open(self.serial_file_path, mode='a+')
            serial_file.write(line_join(time_log, msg))
            serial_file.close()

    def error(self, msg):
        # start log if first time
        if not self.is_start:
            self.start()
        log_file = open(self.log_file_path, mode='a+', encoding='utf-8')
        print('\033[31m%s\033[0m' % msg)
        time_log, time_str, random_str = random_id()
        log_file.write(line_join(time_log, msg))
        log_file.close()
        self.log_info_list.append(line_join(time_log, msg))
        self.end(status='fail')
    
    def end(self, status='pass'):
        # start log if first time
        if not self.is_start:
            self.start()
        self.write_html_file(status)
        if status == 'pass':
            print('\033[37;42mcase %s end...\033[0m' % self.case_name)
        else:
            print('\033[37;41mcase %s end...\033[0m' % self.case_name)
        # print(r'case %s end...' % self.case_name)
        print(r'------------------------------------------------------------')
        case_dir = Path.parent(CASE_PATH)
        SummaryLogger.write({"time":Timer.strftime("%Y%m%d_%H%M%S", self.start_time),"name":self.case_name,"dir":case_dir, "path":CASE_PATH, "url":self.html_file_path,"status":status})
        #open browser
        #webbrowser.open_new_tab(self.html_file_path)
        Command.exit(0)
        
    def write_html_file(self, status):
        log_info_list = self.log_info_list
        # time consuming
        consuming_time = Timer.time() - self.start_time
        with open(self.html_file_path, mode='a+', encoding='utf-8') as html_file:
            html_file.write('<meta http-equiv="Content-Type" content="text/html;charset=utf-8">')
            html_file.write('<body style="width:80%;margin-left:10%;">')
            if status == 'pass':
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
            for i, log in enumerate(log_info_list):
                html_file.write('<div>')
                if log.find(r'[androidtest]') != -1:
                    count = count + 1
                    html_file.write('<div id="step%d" style="background: #6ab0de;box-shadow: 0px 0px 5px #888888; margin-top:20px;color:#ffffff;height:40px;line-height:40px;font-size:18px;padding-left:20px;">[Step%d] %s</div>' % (count, count, log.replace(r'[androidtest]', '')))
                    steps.append({'step':count,'status':'success'})
                elif log.find(r'[matching]') != -1:
                    if (i < len(log_info_list)-1 and log_info_list[i+1].find(r'[androidtest]') != -1) or i == len(log_info_list)-1:
                        matchObj = {}
                        # window
                        if PATHSEP == '\\':
                            matchObj = Json.loads(log[33:].replace('\\', r'\\'))
                        else:# linux
                            matchObj = Json.loads(log[33:])
                        html_file.write('<div style="box-shadow: 0px 0px 5px #888888;">')
                        html_file.write('<div style="padding-left:20px;font-weight:blod;">Target:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="%s"></img></div>' % matchObj['template'])
                        html_file.write('<div style="margin-top:10px;padding-left:20px;font-weight:blod;">Screencap: <img src="%s"></img></div>' % matchObj['screencap'])
                        if matchObj['exists'] == 'True':
                            html_file.write('<div style="margin-top:10px;padding-left:20px;font-weight:blod;">Confidence: %s</div>' % confidence_precent(matchObj['confidence']))
                            html_file.write('<div style="background: #e7f2fa;height:40px;line-height:40px;padding-left:20px;margin-top:10px;font-weight:blod;">Target picture is in screen</div>')
                        else:
                            html_file.write('<div style="background: #e7f2fa;height:40px;line-height:40px;padding-left:20px;margin-top:10px;font-weight:blod;">Target picture is not in screen</div>')
                        html_file.write('</div>')
                elif log.find(r'[tesseract]') != -1:
                    if (i < len(log_info_list)-1 and log_info_list[i+1].find(r'[androidtest]') != -1) or i == len(log_info_list)-1:
                        matchObj = {}
                        # window
                        if PATHSEP == '\\':
                            str = log[34:].replace('\\', r'\\')
                            matchObj = Json.loads(log[34:].replace('\\', r'\\'))
                        else:# linux
                            matchObj = Json.loads(log[34:])
                        html_file.write('<div style="box-shadow: 0px 0px 5px #888888;">')
                        html_file.write('<div style="padding-left:20px;font-weight:blod;">Target:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="%s"></img></div>' % matchObj['template'])
                        html_file.write('<div style="margin-top:10px;padding-left:20px;font-weight:blod;">Screencap: <img src="%s"></img></div>' % matchObj['screencap'])
                        html_file.write('<div style="background: #e7f2fa;padding-left:20px;line-height:30px;margin-top:10px;font-weight:blod;">Recognition result: %s</div>' % matchObj['result'])
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