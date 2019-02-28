#!/usr/bin/env python3

import os
import argparse

def check_exist(dest):
    return os.path.exists(dest)

def check_hardlink(src):
    return os.stat(src).st_nlink > 1

def check_symlink(src):
    return os.path.islink(src)

def check_update(src, dest):
    time_src = os.stat(src).st_mtime
    time_dest = os.stat(src).st_mtime
    return time_src < time_dest


def regularWrite(source, destination, string = ''):
    f_source = os.open(source, os.O_RDONLY)
    f_destination = os.open(destination + string, os.O_CREAT | os.O_WRONLY)
    content = os.read(f_source, os.stat(source).st_size)
    os.write(f_destination, content)
    os.close(f_source)
    os.close(f_destination)


def set_default(source, destination):
    f_source_stat = os.stat(source)
    os.utime(destination, (f_source_stat.st_atime, f_source_stat.st_mtime))
    os.chmod(destination, f_source_stat.st_mode)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--checksum", help = "skip based on checksum, not mod-time & size", action="store_true")
    parser.add_argument("-u", "--update", help = 'skip files that are newer on the receiver', action="store_true")
    parser.add_argument("-r", "--recursive", help = "copy multifile", action="store_true")
    parser.add_argument("source", nargs="+", help = "file source")
    parser.add_argument("destination", help = 'file destination')
    args = parser.parse_args()
    #  create directory if it not exist
    if args.recursive and not check_exist(args.destination):
        os.mkdir(args.destination)

    for element in args.source:
        #  check sym link and hard link
        if not os.path.exists(element):
             print('rsync: link_stat ' + os.path.abspath(element) + 'failed: No such file or directory(2)')
             break
        elif check_symlink(element) or check_hardlink(element):
            #  delete file if it have exist
            if check_exist(args.destination):
                os.unlink(args.destination)

            if check_symlink(element):
                os.symlink(os.readlink(element), args.destination)
            else:
                os.link(element, args.destination)
        elif os.path.isdir(args.destination):
            regularWrite(element, args.destination + '/' + element)
        else:
            regularWrite(element, args.destination)

        set_default(element, args.destination)
