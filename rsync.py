import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--time", help = "not modifier time", action="store_true")
parser.add_argument('-p', '--permission', help = 'not change permission', action="store_true")
parser.add_argument("source", help = "file source")
parser.add_argument("destination", help = 'file destination')
args = parser.parse_args()
if args.time and args.permission:
    pass
if args.time or args.permission:
    pass
else:
    f_source = os.open(args.source, os.O_RDONLY)
    f_source_stat = os.stat(args.source).st_size
    f_destination = os.open(args.destination, os.O_CREAT | os.O_WRONLY)
    content = os.read(f_source, f_source_stat)
    os.write(f_destination, content)
