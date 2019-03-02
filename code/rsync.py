#!/usr/bin/env python3

import os
import argparse


def check_size(src, dest):
    return os.path.getsize(src) == os.path.getsize(dest)


def check_time(src, dest):
    return os.stat(src).st_mtime == os.stat(dest).st_mtime


def check_update(src, dest):
    time_src = os.stat(src).st_mtime
    time_dest = os.stat(src).st_mtime
    return time_src < time_dest


def check_sum(src, dest):
    md5_src = hashlib.md5(src).hexdigest()
    md5_dst = hashlib.md5(dst).hexdigest()
    return md5_src == md5_dst


def symlink(src, dest):
    if os.path.exists(dest) and not os.path.isdir(dest):
        os.unlink(dest)
    if os.path.isdir(dest):
        os.symlink(os.readlink(src), dest + '/' + src.split('/')[-1])
    else:
        os.symlink(os.readlink(src), dest)


def hardlink(src, dest):
    if os.path.exists(dest) and not os.path.isdir(dest):
        os.unlink(dest)
    if os.path.isdir(dest):
        os.link(src, dest + '/' + src.split('/')[-1])
    else:
        os.link(src, dest)


def handling_error(source):
    try:
        f = os.open(source, os.O_RDONLY)
    except FileNotFoundError:
        print('rsync: link_stat "' + os.path.abspath(source) +
              '" failed: No such file or directory (2)')
        return True
    except PermissionError:
        print('rsync: send_files failed to open "' +
              os.path.abspath(source) + '": Permission denied (13)')
        return True
    else:
        os.close(f)
        return False


def copy(source, destination):
    f_source = os.open(source, os.O_RDONLY)
    f_dest = os.open(destination, os.O_CREAT | os.O_WRONLY)
    source_content = os.read(f_source, os.path.getsize(source))
    os.write(f_dest, source_content)
    os.close(f_dest)
    os.close(f_source)
    set_default(source, destination)


def update_content(source, destination):
    file1 = os.open(source, os.O_RDONLY)
    src_content = os.read(file1, os.path.getsize(source))
    file2 = os.open(destination, os.O_RDWR | os.O_CREAT)
    dest_content = os.read(file2, os.path.getsize(destination))
    count = 0
    while count < os.path.getsize(source):
        os.lseek(file1, count, 0)
        os.lseek(file2, count, 0)
        if count < len(dest_content):
            if dest_content[count] != src_content[count]:
                os.write(file2, os.read(file1, 1))
        else:
            os.write(file2, os.read(file1, 1))
        count += 1
    os.close(f_dest)
    os.close(f_source)
    set_default(source, destination)


def set_default(source, destination):
    f_source_stat = os.stat(source)
    os.utime(destination, (f_source_stat.st_atime, f_source_stat.st_mtime))
    os.chmod(destination, f_source_stat.st_mode)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--checksum",
                        action="store_true",
                        help="skip based on checksum, not mod-time & size")
    parser.add_argument("-u", "--update",
                        action="store_true",
                        help='skip files that are newer on the receiver')
    parser.add_argument("-r", "--recursive",
                        action="store_true",
                        help="copy multifile")
    parser.add_argument("source", nargs="+", help="file source")
    parser.add_argument("destination", help='file destination')
    args = parser.parse_args()
    #  create directory if it not exist
    if args.recursive and not check_exist(args.destination):
        os.mkdir(args.destination)

    for item in args.source:
        #  check sym link and hard link
        if handling_error(item):
            break

        if os.stat(item).st_nlink > 1:  # check hard link
            hardlink(item, args.destination)

        elif os.path.islink(item):  # check sym link
            symlink(item, args.destination)

        elif os.path.isdir(args.destination):
            copy(item, args.destination + '/' + item.split('/')[-1])

        elif args.checksum:
            if check_sum(item, args.destination):
                copy(item, args.destination)

        elif args.update:
            if check_update(item, args.destination):
                copy(item, args.destination)

        elif os.path.exists(args.destination):
            if not check_size(item, args.destination) or \
               not check_time(item, args.destination):
                if os.path.getsize(item) >= os.path.getsize(args.destination):
                    update_content(item, args.destination)
                else:
                    os.unlink(args.destination)
                    copy(item, args.destination)
        else:
            copy(item, args.destination)
