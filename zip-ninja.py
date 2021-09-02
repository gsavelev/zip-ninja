#!/usr/bin/env python3

import re
from os import path
import subprocess as s


def split_paths(user_input: str):
    paths_list = re.split(r'(?<!\\) ', user_input)
    return paths_list


def split_zip(paths_list):
    name_ext = path.basename(paths_list[0])
    name, _ = path.splitext(name_ext)
    par_dir = path.dirname(paths_list[0])

    # todo calc amount of stout dots to ETA
    s.call(f'zip -dg -s 20g -j {par_dir}/{name_ext} -O {par_dir}/{name}_chunk |\
           pv > /dev/null', shell=True)


def join_zip(paths_list):
    name_ext = path.basename(paths_list[0])
    name, _ = path.splitext(name_ext)
    par_dir = path.dirname(paths_list[0])
    paths_str = ' '.join(paths_list)

    s.call(f'cat {paths_str} | pv > {par_dir}/{name}_joined.zip', shell=True)
    # todo unzip file with pv status bar
    # && unzip {par_dir}/{name}_joined.zip -d {par_dir} | pv > /dev/null


# waiting for paste to get file(-s) path(-es)
_input = input('⇩ Drop file(-s) here ⇩\n')

# split paths to list
paths = split_paths(_input[: -1])  # removes last space after paste

if len(paths) > 1:
    join_zip(paths)
else:
    split_zip(paths)
