import argparse
from .__init__ import MODULE,VERSION
from .tool import LINESEQ,Command
from .client import execute,create,install,startasm

def print_version():
    print('androidautotest {}{}'.format(VERSION, LINESEQ))
    
def print_run_usage():
    print('usage(run options): androidautotest --casedir <CASEDIR> --device <DEVICE> --times <TIMES>')
    
def print_create_usage():
    print('usage(create options): androidautotest --newcase <NEWCASE> --savedir <SAVEDIR>')
    
def main():
    parser = argparse.ArgumentParser(
        prog='androidautotest',
        usage='{}  androidautotest --installdep {}  androidautotest --startasm {}  androidautotest --newcase <NEWCASE> --savedir <SAVEDIR> {}  androidautotest --casedir <CASEDIR> --device <DEVICE> --times <TIMES>'.format(LINESEQ, LINESEQ, LINESEQ, LINESEQ, LINESEQ),
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
    cmd_line_grp = parser.add_argument_group('install dependency')
    cmd_line_grp.add_argument(
        '--installdep', action='store_true',
        help='install dependency of androidautotest'
    )
    cmd_line_grp = parser.add_argument_group('start asm')
    cmd_line_grp.add_argument(
        '--startasm', action='store_true',
        help='start Android Screen Monitor'
    )
    
    cmd_line_grp = parser.add_argument_group('create case')
    cmd_line_grp.add_argument(
        '--newcase',  metavar='<NEWCASE>',nargs=1, type=str,
        help='New case name to create'
    )
    
    cmd_line_grp.add_argument(
        '--savedir', metavar='<SAVEDIR>', nargs=1, type=str,
        help='Path to save new case'
    )
    
    cmd_line_grp = parser.add_argument_group('run case')
    cmd_line_grp.add_argument(
        '--casedir', metavar='<CASEDIR>', nargs=1, type=str,
        help='Case path to run'
    )
    
    cmd_line_grp.add_argument(
        '--device', metavar='<DEVICE>', nargs=1, type=str,
        help='Device to switch'
    )
    cmd_line_grp.add_argument(
        '--times', metavar='<TIMES>', nargs=1, type=int,
        help='Times of case running'
    )
    args = parser.parse_args()
    
    if args.help:
        print_version()
        parser.print_help()
        Command.exit()
    if args.version:
        print_version()
        Command.exit()
        
    if args.casedir and args.device and args.times:
        args = vars(args)
        case_path = args['casedir'][0]
        device_serial_number = args['device'][0]
        run_times = args['times'][0]
        execute(case_path, device_serial_number, run_times)
    elif args.newcase and args.savedir:
        args = vars(args)
        new_case_name = args['newcase'][0]
        save_dir = args['savedir'][0]
        create(new_case_name, save_dir)
    elif args.installdep:
        install()
    elif args.startasm:
        startasm()
    elif args.casedir or args.device or args.times:
        print_run_usage()
        Command.exit()
    elif args.newcase or args.savedir:
        print_create_usage()
        Command.exit()
    else:
        parser.print_help()
        Command.exit()

    
if __name__ == '__main__':
    main()

