#!/usr/bin/env python3
"""
After using sync.py to download v8 source, this helper will call gn to build
it given OS (android, windows, linux, etc.), architecture (arm, arm64, etc.)
"""
import argparse
import json
import os
import subprocess
import sys

this_dir_path = os.path.dirname(os.path.realpath(__file__))
third_party = 'third_party'

def read_as_json(file_path):
    with open(file_path, mode='r') as file:
        return json.load(file, encoding='UTF-8')


def build_v8(target_arch, build_type, target_platform):
    """Build v8_monolith library.

    Arguments:
        target_arch - usually 'arm', 'ia32' or 'x64'
        build_type - 'release' or 'debug'
        target_platform - either 'android' or sys.platform
    """
    working_dir = os.path.join(this_dir_path, third_party, 'v8')
    output_dir = os.path.abspath(os.path.join('build', '.'.join([target_platform, target_arch, build_type])))
    call_gn = [os.path.join('..', 'depot_tools', 'gn')]
    env = os.environ.copy()
    if sys.platform == 'win32':
        env['DEPOT_TOOLS_WIN_TOOLCHAIN'] = '0'
        call_gn[0] = call_gn[0] + '.bat'
        call_gn[:0] = ['cmd', '/C']

    args_library = read_as_json('args-library.json')
    args_os = {'win32': 'windows', 'darwin': 'osx', 'linux': 'linux', 'android': 'android'}
    gn_args = args_library['common'].copy()
    for args_part in [args_os[target_platform], target_arch, build_type]:
        if args_part not in args_library:
            continue
        gn_args.update(args_library[args_part])

    def stringify(value):
        if isinstance(value, str):
            return value
        if isinstance(value, bool):
            return 'true' if value else 'false'

    args = ' '.join('{}={}'.format(kv[0], stringify(kv[1])) for kv in gn_args.items())
    cmd = call_gn + ['gen', output_dir, '--args=' + args]
    subprocess.run(cmd, cwd=working_dir, env=env, check=True)
    subprocess.run([os.sep.join([third_party, 'depot_tools', 'ninja']), '-C', output_dir, 'v8_monolith'],
                   cwd=this_dir_path, env=env, check=True)


def add_build_v8_parser(subparsers, option_name, arches, build_types):
    subparser = subparsers.add_parser(option_name)
    subparser.add_argument('target_arch', choices=arches,
            help='The target architecture')
    subparser.add_argument('build_type', choices=build_types,
            help='The build mode')
    subparser.set_defaults(func=lambda args: build_v8(args.target_arch, args.build_type, option_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(help='Target platform')
    add_build_v8_parser(subparsers, 'windows', ['i32', 'x64'], ['debug', 'release'])
    add_build_v8_parser(subparsers, 'linux', ['ia32', 'x64'], ['debug', 'release'])
    add_build_v8_parser(subparsers, 'android', ['arm', 'arm64', 'ia32', 'x64'], ['debug', 'release'])
    args = parser.parse_args()
    args.func(args)
