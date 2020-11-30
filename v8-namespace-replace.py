#!/usr/bin/env python3
"""
This script replaces lines in v8 __config source code file, it is
necessary for both replace the namespace pre compile and
revert that after compile.
"""
import argparse
import os
import subprocess
import sys

this_dir_path = os.path.dirname(os.path.realpath(__file__))
third_party = 'third_party'

namespace_file = third_party + \
    "/v8/buildtools/third_party/libc++/trunk/include/__config"

src_changes = {
    "# define _LIBCPP_ABI_NAMESPACE _LIBCPP_CONCAT(__,_LIBCPP_ABI_VERSION)" :
    "# define _LIBCPP_ABI_NAMESPACE _LIBCPP_CONCAT(__ndk,_LIBCPP_ABI_VERSION)"
}

def exit_with(message):
    print(message)
    sys.exit(1)

def replace_str_in_file(filepath, src, dst):
    _file = open(filepath, "r")
    lines = _file.readlines()
    _file.close()

    _file = open(filepath, "w")
    n_replaced_lines = 0
    for line in lines:
        if src in line:
            new_line = line.replace(src, dst)
            if new_line != line:
                n_replaced_lines += 1
            line = new_line
        _file.write(line)
    _file.close()
    return n_replaced_lines

def replace_namespace():
    """
    Current v8 namespace might not be compatible with our solution of ndk
    We need to search and replace, this needs to run after sync
    """
    for src in src_changes:
        n_replaced_lines = replace_str_in_file(namespace_file, src, src_changes[src])
        # if it did not need to replace probably this workaround is not needed
        # anymore so we need to stop build and send info message
        if n_replaced_lines == 0:
            exit_with('Wasn\'t possible to replace namespace in v8 please check \
            if this workaround is is necessary')

def revert_replace_namespace():
    """
    At the end of compilation we need to revert the namespace change
    """
    for src in src_changes:
        replace_str_in_file(namespace_file, src_changes[src], src)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--action', help='action to perform either \'replace\' \
                        or \'revert\' namespace in fetched v8 code',
                        type=str, default="replace")
    parser.add_argument('--os', help='os that is the source code target',
                        type=str, default="android")

    args = parser.parse_args()
    if args.os.lower() != "android":
        pass
    elif args.action.lower() == "replace":
        replace_namespace()
    elif args.action.lower() == "revert":
        revert_replace_namespace()
