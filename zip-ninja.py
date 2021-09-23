#!/usr/bin/env python3

import re
import argparse
from os import path
import subprocess as s


def split_paths(user_input: str):
    paths_list = re.split(r'(?<!\\) ', user_input)
    return paths_list


def split_zip(paths_list, output_path):
    name_ext = path.basename(paths_list[0])
    name, _ = path.splitext(name_ext)
    par_dir = path.dirname(paths_list[0])
    out_dir = par_dir

    if output_path:
       out_dir = output_path

    # todo calc amount of stout dots to ETA
    s.call(f'zip -dg -s 20g -j {par_dir}/{name_ext} -O {out_dir}/{name}_chunk |\
           pv > /dev/null', shell=True)


def join_zip(paths_list, output_path):
    name_ext = path.basename(paths_list[0])
    name, _ = path.splitext(name_ext)
    par_dir = path.dirname(paths_list[0])
    paths_str = ' '.join(paths_list)

    out_dir = par_dir

    if output_path:
        out_dir = output_path

    s.call(f'cat {paths_str} | pv > {out_dir}/{name}_joined.zip', shell=True)
    # todo unzip file with pv status bar
    # && unzip {par_dir}/{name}_joined.zip -d {par_dir} | pv > /dev/null


custom_output_path = None
description = 'Script splits fat archive into several parts' \
              'also combines several parts back to fat one.'

# init argument parser
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-o', '--output', help='set custom output path')

# read arguments
args = parser.parse_args()

# check for --output or -o
if args.output:
    custom_output_path = args.output

# waiting for paste to get file(-s) path(-es)
_input = input('⇩ Drop file(-s) here ⇩\n')

# split file_paths to list
file_paths = split_paths(_input[: -1])  # removes last space after paste

if len(file_paths) > 1:
    join_zip(paths_list=file_paths,
             output_path=custom_output_path)
else:
    split_zip(paths_list=file_paths,
              output_path=custom_output_path)
