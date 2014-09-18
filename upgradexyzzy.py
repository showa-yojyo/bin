#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script fetches the current Xyzzy archive from xyzzy-022.github.com
and installs on your machine.

Example:
   You run this script without arguments::

   $ python upgradexyzzy.py
"""

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from distutils.dir_util import copy_tree
import os
import shutil
import sys
import urllib.request
import urllib.error
import urllib.parse
import zipfile

__version__ = '1.1.0'

XYZZY_GITHUB_URL = r'http://xyzzy-022.github.io/'

# TODO: user settings
XYZZY_DEST = r'D:/Program Files/xyzzy/'
WORK_DIR = r'D:/Temp/'

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='Xyzzy Manager')
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='a lot more information output')

    return parser.parse_args()

def get_xyzzy_url():
    """Get the URL of the current Xyzzy archive (ZIP) file.

    Returns:
        The URL of xyzzy-X.Y.Z.zip.
    """

    url = XYZZY_GITHUB_URL
    html = urllib.request.urlopen(url).read()

    # <div class="download">
    # <a href="/downloads/xyzzy-0.2.2.253.zip">
    # ...
    # </a>
    # </div>
    soup = BeautifulSoup(html)
    zipurl = soup.find('div', class_='download').find('a')['href']

    if zipurl.startswith('http://') or zipurl.startswith('https://'):
        pass
    elif zipurl.startswith('/'):
        zipurl = urllib.parse.urljoin(XYZZY_GITHUB_URL, zipurl)

    # e.g. 'http://xyzzy-022.github.io/xyzzy-022/xyzzy/xyzzy-0.2.2.253.zip'
    return zipurl

def download_xyzzy(args, zipurl, workdir):
    """Download the current Xyzzy archive (ZIP) file from the website.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.
        zipurl: URL of xyzzy-X.Y.Z.zip.
        workdir: Path to user's working directory.

    Returns:
        The path of xyzzy-X.Y.Z.zip downloaded.
    """

    if args.verbose:
        print('Downloading: {0}...'.format(zipurl), file=sys.stderr)

    localfile = urllib.request.urlopen(zipurl)

    if args.verbose:
        print('Done.', file=sys.stderr)

    # e.g. 'xyzzy-0.2.2.253.zip'
    zipname = os.path.basename(zipurl)
    zippath = os.path.join(workdir, zipname)
    if os.path.exists(zippath):
        return zippath

    # Save the zip file to workdir
    with open(zippath, 'wb') as fout:
        fout.write(localfile.read())

    return zippath

def overwrite_xyzzy(workdir, destdir):
    """Overwrite with new Xyzzy packages.

    Args:
        workdir: Path to user's working directory.
        destdir: Xyzzy's directory, i.e. $XYZZYHOME.

    Returns:
        The path of xyzzy-X.Y.Z.zip downloaded.
    """

    xyzzysrc = os.path.join(workdir, 'xyzzy')
    copy_tree(xyzzysrc, destdir)
    return xyzzysrc, destdir

def main(args):
    """The main function.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """
    zipurl = get_xyzzy_url()
    if args.verbose:
        print('URL: {}'.format(zipurl), file=sys.stderr)

    zippath = download_xyzzy(args, zipurl, WORK_DIR)
    if args.verbose:
        print('Saved to: {}'.format(zippath), file=sys.stderr)

    # Extract the archive and overwrite to XYZZY_DEST.
    with zipfile.ZipFile(zippath, 'r') as arch:
        arch.extractall(WORK_DIR)

    xyzzysrc, xyzzyhome = overwrite_xyzzy(WORK_DIR, XYZZY_DEST)
    if args.verbose:
        print('Copied {0} to {1}...'.format(xyzzysrc, xyzzyhome))

    # Clean up temporary files.
    if args.verbose:
        print('Delete {}...'.format(zippath), file=sys.stderr)
    os.remove(zippath)

    if args.verbose:
        print('Delete {}...'.format(xyzzysrc), file=sys.stderr)
    shutil.rmtree(xyzzysrc)

    if args.verbose:
        print('Finished.', file=sys.stderr)

if __name__ == '__main__':
    main(configure())
