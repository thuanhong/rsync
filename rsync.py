import os
import argparse


def main(source, destination, time = True, per = True)
    f_source = os.open(source, os.O_RDONLY)
    f_source_stat = os.stat(source)
    f_destination = os.open(destination, os.O_CREAT | os.O_WRONLY)
    content = os.read(f_source, f_source_stat.st_size)
    os.write(f_destination, content)
    if time:
        f_source_stat

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", help = "not modifier time", action="store_true")
    parser.add_argument('-p', '--permission', help = 'not change permission', action="store_true")
    parser.add_argument("source", help = "file source")
    parser.add_argument("destination", help = 'file destination')
    args = parser.parse_args()

    if args.time and args.permission:
        main(args.source, args.destination, time = False, per = False)
    elif args.time:
        main(args.source, args.destination, time = False)
    elif args.permission:
        main(args.source, args.destination, per = False)
    else:
        main(args.source, args.destination)
