#!/usr/bin/env python3

import argparse
from pathlib import Path
import subprocess
import sys

def recent(root=None, ndays=7):
    '''
    List modification time and absolute path of every file below the given root
    directory that has been modified in the last ndays days. The list is in
    reverse chronological order, i.e. the most recently modified file is listed
    first. Each line starts with the modification time stamp, ISO 8601
    formatted, in minute resolution, followed by a single space and the
    absolute path. For example:

    2022-02-14 20:41 /home/cb/sync/private/organizer/todo/todo.md

    If no root is given, the current working directory is used. Also, root may
    be a relative path below the working directory.

    If ndays is not explicitely given, the last 7 days are used.

    Dotfiles and files inside .git/ directories are ignored. TODO: Make this
    configurable.

    Implementation note: This utility is basically a thin wrapper around the 
    find command. When find encounters a subdirectory to which the user has no
    access, it prints a "Permission denied" warning to stderr. To suppress
    these warnings, all errors raised by find are redirected to /dev/null.
    '''
    root = root or Path.cwd()
    try:
        root = Path(root).resolve(strict=True)
    except FileNotFoundError:
        raise
    assert root.is_dir()
    assert isinstance(ndays, int) and ndays > 0
    subprocess.run(
        f"find {root} -type f -not -path '*/.*' -not -path '*.git/*' -mtime -{ndays} -printf '%TY-%Tm-%Td %TH:%TM %p\n' 2>/dev/null | sort -r",
        shell=True)

def main():
    '''
    Handle command line arguments for the recent() function.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'root',
        nargs = '?',
        default = Path.cwd(),
        help = 'root directory')
    parser.add_argument(
        '-n',
        '--ndays',
        type = int,
        default = 7,
        help = 'number of days in the past')
    args = parser.parse_args()
    recent(root=args.root, ndays=args.ndays)

if __name__ == '__main__':
    main()
