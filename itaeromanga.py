#!/usr/bin/env python

"""itaeromanga.py (no comment)
"""

import os.path
import sys
from bs4 import BeautifulSoup
import requests

def download_image(url):
    """Equivalent to `wget url`
    """

    response = requests.get(url)
    with open(os.path.basename(url), 'wb') as output:
        output.write(response.content)

def main(args=sys.argv):
    """No description provided
    """

    if len(args) < 1:
        print('Error: no url')
        sys.exit(1)

    # download html
    url = args[1]
    response = requests.get(url)

    b = BeautifulSoup(response.content, 'lxml')
    img = b.select('section > img')

    # list urls for wget
    for i in img:
        url = i["src"]
        print(url)

    # download all files in img
    # TODO: async version
    #download_image(url)

if __name__ == "__main__":
    main()
