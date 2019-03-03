#!/usr/bin/env python3

import os
import argparse
import hashlib


def check_size(src, dest):
    return os.path.getsize(src) == os.path.getsize(dest)


def check_time(src, dest):
    return os.stat(src).st_mtime == os.stat(dest).st_mtime


def check_update(src, dest):
    time_src = os.stat(src).st_mtime
    time_dest = os.stat(src).st_mtime
    return time_src < time_dest


def check_sum(src, dest):
    md5_src = hashlib.md5(src.encode()).hexdigest()
    md5_dest = hashlib.md5(dest.encode()).hexdigest()
    return md5_src == md5_dest


def symlink(src, dest):
    '''
    copy symlinks as symlinks
    '''
    if os.path.exists(dest) and not os.path.isdir(dest):
        os.unlink(dest)
    if os.path.isdir(dest):
        os.symlink(os.readlink(src), dest + '/' + src.split('/')[-1])
    else:
        os.symlink(os.readlink(src), dest)


def hardlink(src, dest):
    '''
    preserve hard links
    '''
    if os.path.exists(dest) and not os.path.isdir(dest):
        os.unlink(dest)
    if os.path.isdir(dest):
        os.link(src, dest + '/' + src.split('/')[-1])
    else:
        os.link(src, dest)


def handling_error(source):
    '''
    catch error
    '''
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
    '''
    Rewrite content
    '''
    f_source = os.open(source, os.O_RDONLY)
    f_dest = os.open(destination, os.O_CREAT | os.O_WRONLY)
    source_content = os.read(f_source, os.path.getsize(source))
    os.write(f_dest, source_content)
    os.close(f_dest)
    os.close(f_source)
    set_default(source, destination)


def update_content(source, destination):
    '''
    only copy the parts that are different
    between the source file and the destination file
    '''
    # open and read content of 2 file
    file1 = os.open(source, os.O_RDONLY)
    src_content = os.read(file1, os.path.getsize(source))
    file2 = os.open(destination, os.O_RDWR | os.O_CREAT)
    dest_content = os.read(file2, os.path.getsize(destination))
    count = 0
    # rewrite the parts that are different
    while count < os.path.getsize(source):
        os.lseek(file1, count, 0)
        os.lseek(file2, count, 0)
        if count < len(dest_content):
            if dest_content[count] != src_content[count]:
                os.write(file2, os.read(file1, 1))
        else:
            os.write(file2, os.read(file1, 1))
        count += 1

    os.close(file1)
    os.close(file2)
    set_default(source, destination)


def set_default(source, destination):
    '''
    Set mod time and permission for the destination file1
    '''
    f_source_stat = os.stat(source)
    os.utime(destination, (f_source_stat.st_atime, f_source_stat.st_mtime))
    os.chmod(destination, f_source_stat.st_mode)


def recursive(item, dest):
    # path = []
    # for root, dirs, files in os.walk(".", topdown = True):
    #    for name in files:
    #       path.append(os.path.join(root, name))
    #    for name in dirs:
    #       path.append(os.path.join(root, name))
    for element in list:
        if os.path.isdir(element):
            os.mkdir(dest + '/' + element)
            recursive(element, dest + '/' + element)
        else:
            main(item, dest)


def main(item, dest):
    '''
    handle main
    '''
    if os.stat(item).st_nlink > 1:  # check hard link
        hardlink(item, dest)

    elif os.path.islink(item):  # check sym link
        symlink(item, dest)

    elif os.path.isdir(dest):  # if the destination is directory
        copy(item, dest + '/' + item.split('/')[-1])

    elif args.checksum:  # -c option
        if check_sum(item, dest):
            copy(item, dest)

    elif args.update:  # -u option
        if check_update(item, dest):
            copy(item, dest)

    elif os.path.exists(dest):  # rewrite all or rewrite the parts different
        if not check_size(item, dest) or \
           not check_time(item, dest):
            if os.path.getsize(item) >= os.path.getsize(dest):
                update_content(item, dest)
            else:
                os.unlink(dest)
                copy(item, dest)
    else:
        copy(item, dest)


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
    if args.recursive and not os.path.exists(args.destination):
        os.mkdir(args.destination)

    for item in args.source:
        if handling_error(item):
            break

        if args.recursive and os.path.isdir(item):
            recursive(item, args.destination)
        else:
            main(item, args.destination)
