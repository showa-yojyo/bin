# -*- coding: utf-8 -*-
u"""
Copyright (c) 2012 プレハブ小屋 <yojyo@hotmail.com>
All Rights Reserved.  NO WARRANTY.

最新版の Xyzzy をダウンロードして、所定のパスに解凍する。
"""

from BeautifulSoup import BeautifulSoup
from distutils.dir_util import copy_tree

import os
import shutil
import urllib2
import zipfile

XYZZY_GITHUB_URL = r'http://xyzzy-022.github.com/'

# TODO: user settings
XYZZY_DEST = r'C:/Program Files/xyzzy/'
WORK_DIR = r'D:/Temp/'

def get_latest_xyzzy_url():
    url = XYZZY_GITHUB_URL
    html = urllib2.urlopen(url).read()

    # <div class="download">
    # <a href="https://github.com/downloads/xyzzy-022/xyzzy/xyzzy-0.2.2.241.zip">
    # ...
    # </div>
    soup = BeautifulSoup(html)
    div = soup.findAll('div', attrs={'class':'download'})
    a = div[0].find('a')
    zipurl = a['href']

    # e.g. 'https://github.com/downloads/xyzzy-022/xyzzy/xyzzy-0.2.2.241.zip'
    return zipurl

def download_xyzzy(zipurl, workdir):
    f = urllib2.urlopen(zipurl)
    print 'Download: {0}: done.'.format(zipurl)

    # e.g. 'xyzzy-0.2.2.241.zip'
    zipname = os.path.basename(zipurl)
    zippath = os.path.join(workdir, zipname)
    if os.path.exists(zippath):
        return zippath

    # Save the zip file to workdir
    with open(zippath, 'wb') as fout:
        fout.write(f.read())

    return zippath

def overwrite_xyzzy(workdir, destdir):
    xyzzysrc = os.path.join(workdir, 'xyzzy')
    copy_tree(xyzzysrc, destdir)
    return xyzzysrc, destdir

def main():
    zipurl = get_latest_xyzzy_url()

    zippath = download_xyzzy(zipurl, WORK_DIR)
    print 'Saved to: {0}'.format(zippath)

    # Extract the archive and overwrite to XYZZY_DEST.
    arch = zipfile.ZipFile(zippath, 'r')
    arch.extractall(WORK_DIR)
    arch.close()

    xyzzysrc, xyzzyhome = overwrite_xyzzy(WORK_DIR, XYZZY_DEST)
    print 'Copied {0} to {1}...'.format(xyzzysrc, xyzzyhome)

    # Clean up temporary files.
    print 'Delete {0}'.format(zippath)
    os.remove(zippath)
    print 'Delete {0}'.format(xyzzysrc)
    shutil.rmtree(xyzzysrc)

    print 'Finished.'

if __name__ == '__main__':
    main()
