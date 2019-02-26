import os
import argparse


def regularWrite(source, destination, update = False, check = False):
    f_source = os.open(source, os.O_RDONLY)
    f_destination = os.open(destination, os.O_CREAT | os.O_WRONLY)
    content = os.read(f_source, f_source_stat.st_size)
    os.write(f_destination, content)
    os.close(f_source)
    os.close(f_destination)
    set_default(source, destination)



def set_default(source, destination):
    f_source_stat = os.stat(source)
    os.utime(destination, (f_source_stat.st_atime, f_source_stat.st_mtime))
    os.chmod(destination, f_source_stat.st_mode)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--checksum", help = "skip based on checksum, not mod-time & size", action="store_true")
    parser.add_argument("-u", "--update", help = 'skip files that are newer on the receiver', action="store_true")
    parser.add_argument("source", help = "file source")
    parser.add_argument("destination", help = 'file destination')
    args = parser.parse_args()

    if args.update:
        main(args.source, args.destination, update = True)
    elif args.checksum:
        main(args.source, args.destination, check = True)
    else:
        main(args.source, args.destination)
