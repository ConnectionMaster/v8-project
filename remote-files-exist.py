#!/usr/bin/env python3
"""
Given a list of urls as arguments, the program will succeed if they are all
existing and reacheable.
"""
import requests
import sys

def check_urls(url_list):
    for url in url_list:
        req = requests.head(url)
        if not req.ok:
            sys.stderr.write("URL %s returned %s\n" % (url, req.status_code))
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip().replace('\n', ' '))
        sys.exit(1)
    check_urls(sys.argv[1:])
