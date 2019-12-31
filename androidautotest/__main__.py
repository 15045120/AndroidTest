import argparse
from .__init__ import MODULE,VERSION
from .tool import LINESEQ,Command
from .client import execute

def print_version():
    print('androidautotest {}{}'.format(VERSION, LINESEQ))
    
def print_usage():
    print('androidautotest [--casedir CASEDIR] [--device DEVICE] [--times TIMES]')
    
def main():
    parser = argparse.ArgumentParser(
        prog='androidautotest',
        usage='androidautotest [--casedir CASEDIR] [--device DEVICE] [--times TIMES]',
        description='A framework to run test case for android automated test',
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
        '--casedir', metavar='CASEDIR', nargs=1, type=str,
        help='Case path to run'
    )
    
    cmd_line_grp.add_argument(
        '--device', metavar='DEVICE', nargs=1, type=str,
        help='Device to switch'
    )
    cmd_line_grp.add_argument(
        '--times', metavar='TIMES', nargs=1, type=int,
        help='Times of case running'
    )
    args = parser.parse_args()
    
    if not args.help and not args.version and not args.casedir and not args.device and not args.times:
        print_version()
        parser.print_help()
        Command.exit()
    if args.help:
        print_version()
        parser.print_help()
        Command.exit()
    if args.version:
        print_version()
        Command.exit()
        
    args = vars(args)
    case_path = args['casedir'][0]
    device_serial_number = args['device'][0]
    run_times = args['times'][0]
    execute(case_path, device_serial_number, run_times)
    
if __name__ == '__main__':
    main()

