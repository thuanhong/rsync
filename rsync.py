#!/usr/bin/env python3

import os
import argparse


def regularWrite(src, dest):
    if os.path.islink(src):
        os.symlink(os.readlink(src), dest)
    #  open source file and destination file
    f_src = os.open(src, os.O_RDONLY)
    if os.path.isdir(args.dest):
        dest  = dest + '/' + src
    f_dest = os.open(dest, os.O_CREAT | os.O_WRONLY)

    f_src_stat = os.stat(src)
    content = os.read(f_src, f_src_stat.st_size)
    os.write(f_dest, content)
    os.close(f_src)
    os.close(f_dest)
    #  set default time and permission
    os.utime(dest, (f_src_stat.st_atime, f_src_stat.st_mtime))
    os.chmod(dest, f_src_stat.st_mode)
    #  set default symlink and hardlink



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--checksum", help = "skip based on checksum, not mod-time & size", action="store_true")
    parser.add_argument("-u", "--update", help = 'skip files that are newer on the receiver', action="store_true")
    parser.add_argument("src", help = "file src")
    parser.add_argument("dest", help = 'file dest')
    args = parser.parse_args()

    if os.path.isfile(args.src):
        regularWrite(args.src, args.dest)
    else:
        print('skipping directory new')
