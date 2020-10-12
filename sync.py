#!/usr/bin/env python3
"""
Given a revision (hash of the v8 commit), this fetches the v8 source code and
its dependencies.
"""
import argparse
import os
import subprocess
import sys

depot_tools_repository_url = 'https://chromium.googlesource.com/chromium/tools/depot_tools.git'

this_dir_path = os.path.dirname(os.path.realpath(__file__))
third_party = 'third_party'

def sync(v8_revision):
    """Clones all required code and tools."""
    working_dir = os.path.join(this_dir_path, third_party)
    depot_tools_path = os.sep.join([working_dir, 'depot_tools'])
    # a simple way to ensure that depot_tools exists
    if not os.path.exists(depot_tools_path):
        cmd = ['git', 'clone', depot_tools_repository_url]
        subprocess.run(cmd, cwd=working_dir, check=True)
    env = os.environ.copy()
    env['PATH'] = os.pathsep.join([os.environ['PATH'], depot_tools_path])
    gclient_file = 'gclient-' + ('win' if sys.platform == 'win32' else 'nix')
    cmd_gclient_file = ['--gclientfile', gclient_file]
    call_gclient = ['gclient']
    if sys.platform == 'win32':
        env['DEPOT_TOOLS_WIN_TOOLCHAIN'] = '0'
        call_gclient[0] = call_gclient[0] + '.bat'
        call_gclient[:0] = ['cmd', '/C']
    subprocess.run(call_gclient + ['sync', '--revision', v8_revision] + cmd_gclient_file,
                   cwd=working_dir, env=env, check=True)
    subprocess.run(call_gclient + ['runhooks'] + cmd_gclient_file,
                   cwd=os.sep.join([working_dir, 'v8']), env=env, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('revision', help='The desired v8 source code commit hash')
    args = parser.parse_args()
    sync(args.revision)
