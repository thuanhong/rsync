#!/usr/bin/env python3

import os
import argparse


def check_exist(dest):
    return os.path.exists(dest)


def check_size(src, dest):
    return os.stat(src).st_size == os.stat(src).st_size


def check_time(src, dest):
    return os.stat(src).st_mtime == os.stat(dest).st_mtime


def check_hardlink(src):
    return os.stat(src).st_nlink > 1


def check_symlink(src):
    return os.path.islink(src)


def check_update(src, dest):
    time_src = os.stat(src).st_mtime
    time_dest = os.stat(src).st_mtime
    return time_src < time_dest


def regularWrite(source, destination):
    f_source = os.open(source, os.O_RDONLY)
    f_dest = os.open(destination,os.O_CREAT | os.O_WRONLY)
    source_content = os.read(f_source, os.path.getsize(source))
    os.write(f_dest, source_content)
    os.close(f_dest)
    os.close(f_source)

def update_content(source, destination):
    content_list = []
    fd_source = os.open(source_path, os.O_RDONLY)
    fd_dest = os.open(dest_path, os.O_RDWR)
    source_content = os.read(fd_source, source_size)
    dest_content = os.read(fd_dest, dest_size)
    content_list.append(source_content)
    content_list.append(dest_content)
    cp = common_prefix(content_list)
    os.lseek(fd_dest, len(cp), 0)
    os.write(fd_dest, source_content[len(cp):])
    os.close(fd_dest)
    os.close(fd_source)


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
             print('rsync: link_stat "' + os.path.abspath(element) + '" failed: No such file or directory (2)')
             break
        elif os.path.isdir(element) and not args.recursive:
            print('skipping directory dir')
            break
        elif not os.access(element, os.R_OK):
            print('rsync: send_files failed to open "' + os.path.abspath(element) + '": Permission denied (13)')
            break
        elif check_symlink(element) or check_hardlink(element):
            #  delete file if it have exist
            if check_exist(args.destination) and not os.path.isdir(args.destination):
                os.unlink(args.destination)

            if check_symlink(element):
                if os.path.isdir(args.destination):
                    os.symlink(os.readlink(element), args.destination + '/' + element.split('/')[-1])
                else:
                    os.symlink(os.readlink(element), args.destination)
            else:
                if os.path.isdir(args.destination):
                    os.link(element, args.destination + '/' + element.split('/')[-1])
                else:
                    os.link(element, args.destination)

        elif os.path.isdir(args.destination):
            regularWrite(element, args.destination + '/' + element.split('/')[-1])
            set_default(element, args.destination + '/' + element.split('/')[-1])

        elif args.update:
            if not check_update(element, args.destination):
                regularWrite(element, args.destination)
                set_default(element, args.destination)
        elif not check_size(element, args.destination) or not check_time(element, args.destination):
            if os.path.exists(args.destination):
                update_content(element, args.destination)
            else:
                regularWrite(element, args.destination)
            set_default(element, args.destination)
