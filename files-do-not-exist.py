#!/usr/bin/env python3
"""
Given a list of urls as arguments, the program will fail if they are all
existing and reacheable.
"""
from functools import reduce
import requests
import sys

def check_urls(url_list):
    """Returns true when all the urls exists and are reachable"""
    responses = map(lambda url: requests.head(url).ok, url_list)
    result = reduce(lambda a, b: a and b, responses)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip().replace('\n', ' '))
    else:
        check_urls(sys.argv[1:]) and sys.exit(1)
