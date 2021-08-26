#!/usr/bin/env python3

import re
from os import path
import subprocess as s


def split_paths(user_input: str):
    paths_list = re.split(r'(?<!\\) ', user_input)
    return paths_list


def split_zip(paths_list):
    i_path = paths_list[0]
    f_name = path.basename(i_path)
    p_dir = path.dirname(i_path)

    s.call(f'zip -s 49g -j {p_dir}/{f_name} --out {p_dir}/chunk', shell=True)


def join_zip(paths_list):
    f_name = path.basename(paths_list[0])
    p_dir = path.dirname(paths_list[0])
    paths_str = ' '.join(paths_list)

    s.call(f'cat {paths_str} > {p_dir}/joined.zip &&\
           unzip {p_dir}/joined.zip -d {p_dir}/',
           shell=True)


# waiting for paste to get file(-s) path(-es)
_input = input('⇩ Drop file(-s) here ⇩\n')

# split paths to list
paths = split_paths(_input[: -1])  # removes last space after paste

if len(paths) > 1:
    join_zip(paths)
else:
    split_zip(paths)
