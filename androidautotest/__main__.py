import argparse
import sys
import os
from .__init__ import MODULE,VERSION
from .tool import LINESEQ
from .client import execute

def print_version():
    print('androidautotest {}{}'.format(VERSION, LINESEQ))
    
def print_usage():
    print('androidautotest [-r|--run] <case_path> [-d|--device] <device_serial_number> [-t|--times] <run_times>')
    
def main():
    parser = argparse.ArgumentParser(
        prog='androidautotest',
        usage='androidautotest [-r|--run] <case_path> [-d|--device] <device_serial_number> [-t|--times] <run_times>',
        description='A framework to run test case',
        add_help=False,
    )
    parser.add_argument(
        '-V', '--version', action='store_true',
        help='Print version and exit'
    )
    parser.add_argument(
        '-h', '--help', action='store_true',
        help='Print this help message and exit'
    )
    cmd_line_grp = parser.add_argument_group('cmdlines options')
    cmd_line_grp.add_argument(
        '-c', '--case', metavar='<case_path>', nargs=1, type=str,
        help='Case path to run'
    )
    
    cmd_line_grp.add_argument(
        '-d', '--device', metavar='<device_serial_number>', nargs=1, type=str,
        help='Device to switch'
    )
    cmd_line_grp.add_argument(
        '-t', '--times', metavar='<run_times>', nargs=1, type=int,
        help='Times of case running'
    )
    args = parser.parse_args()
    
    if args.help:
        print_version()
        parser.print_help()
        sys.exit()
    if args.version:
        print_version()
        sys.exit()
        
    if not args.case:
        print('androidautotest: error: miss argument: [-c|--case]')
        sys.exit()
    if not args.device:
        print('androidautotest: error: miss argument: [-d|--device]')
    if not args.times:
        print('androidautotest: error: miss argument: [-t|--times]')
        sys.exit()
    args = vars(args)
    case_path = args['case'][0]
    device_serial_number = args['device'][0]
    run_times = args['times'][0]
    execute(case_path, device_serial_number, run_times)
    
if __name__ == '__main__':
    main()

