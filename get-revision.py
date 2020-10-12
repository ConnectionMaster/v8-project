#!/usr/bin/env python3
"""
Given an OS (Android, Linux, Windows, etc.) and a channel (stable, beta,
canary, dev) print out the v8 commit hash as fetched from omaha proxy
"""
import argparse
import json
from urllib import request

omahaproxy_format='https://omahaproxy.appspot.com/all.json?os={}&channel={}'

def get_revision(os, channel):
    """Get the v8 resision per os and channel"""
    url = omahaproxy_format.format(os, channel)
    response = json.loads(request.urlopen(url).read())
    return response[0]['versions'][0]['v8_commit']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('os', choices=[
        'win', 'win64', 'linux', 'mac', 'cros', 'android', 'webview'
        ])
    parser.add_argument('channel', choices=['stable', 'beta', 'dev', 'canary'])
    args = parser.parse_args()
    revision = get_revision(args.os, args.channel)
    print(revision)
