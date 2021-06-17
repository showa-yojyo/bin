#!/usr/bin/env python

"""
A YouTube playlist simple viewer

Usage: See `laylistdump.py --help

Example:
bash$ playlistdump.py https://www.youtube.com/playlist?list=PLp_NmZC4oOWUMWf6jhyXOMM1vk2Fk7nv6
"""

from argparse import ArgumentParser
import json
import sys
from pytube import request, Playlist

__version__ = '1.0.0'

def extract_videos(initial_data):
    """A modified Playlist._extract_videos

    :param initial_data: Input json extracted from the page or the last
        server response
    :returns: Tuple containing a list of up to 100 video data and
        a continuation token, if more videos are available
    """

    try:
        # this is the json tree structure, if the json was extracted from html
        section_contents = initial_data["contents"][
            "twoColumnBrowseResultsRenderer"][
            "tabs"][0]["tabRenderer"]["content"][
            "sectionListRenderer"]["contents"]
        try:
           # Playlist without submenus
           important_content = section_contents[
               0]["itemSectionRenderer"][
               "contents"][0]["playlistVideoListRenderer"]
        except (KeyError, IndexError, TypeError):
            # Playlist with submenus
            important_content = section_contents[
                1]["itemSectionRenderer"][
                "contents"][0]["playlistVideoListRenderer"]
        videos = important_content["contents"]
    except (KeyError, IndexError, TypeError):
        try:
            # this is the json tree structure, if the json was directly sent
            # by the server in a continuation response
            # no longer a list and no longer has the "response" key
            important_content = initial_data['onResponseReceivedActions'][0][
                'appendContinuationItemsAction']['continuationItems']
            videos = important_content
        except (KeyError, IndexError, TypeError) as p:
            print(p, file=sys.stderr)
            return [], None

    try:
        continuation = videos[-1]['continuationItemRenderer'][
            'continuationEndpoint'
        ]['continuationCommand']['token']
        videos = videos[:-1]
    except (KeyError, IndexError):
        # if there is an error, no continuation is available
        continuation = None

    return ([i['playlistVideoRenderer'] for i in videos], continuation)


def paginate(pl):
    """A modified Playlist._paginate

    :param pl Playlist:
    :returns: Iterable of YouTube video data
    """

    videos, continuation = extract_videos(pl.initial_data)
    yield from videos

    # Extraction from a playlist only returns 100 videos at a time
    # if self._extract_videos returns a continuation there are more
    # than 100 songs inside a playlist, so we need to add further requests
    # to gather all of them
    if continuation:
        load_more_url, headers, data = pl._build_continuation_url(continuation)
    else:
        load_more_url, headers, data = None, None, None

    while load_more_url and headers and data:  # there is an url found
        ##print("load more url: %s", load_more_url)
        # requesting the next page of videos with the url generated from the
        # previous page, needs to be a post
        req = request.post(load_more_url, extra_headers=headers, data=data)
        # extract up to 100 songs from the page loaded
        # returns another continuation if more videos are available
        videos, continuation = extract_videos(json.loads(req))
        yield from videos
        if continuation:
            load_more_url, headers, data = pl._build_continuation_url(continuation)
        else:
            load_more_url, headers, data = None, None, None


def parse_args(args):
    """Parse the command line parameters.

    Most options are taken from GNU wget.

    :param args: Raw command line arguments.
    :rtype: argparse.Namespace
    """

    parser = ArgumentParser(
        description='A YouTube playlist simple viewer',
        epilog='Mail bug reports and suggestions to <yojyo@hotmail.com>',
        add_help=False)

    parser.add_argument(
        'playlist_url',
        metavar='URL',
        help='URL of a playlist')

    # Startup:
    startup_group = parser.add_argument_group('Startup')
    startup_group.add_argument(
        '-V', '--version',
        action='version',
        version=__version__)
    startup_group.add_argument(
        '-h', '--help',
        action='help',
        help='print this help')

    # XXX:
    format_group = parser.add_argument_group('Format')
    format_group.add_argument(
        '-d', '--delimiter',
        metavar='DELIM',
        default='\t',
        nargs=1,
        help='use DELIM instead of TAB for field delimiter')

    return parser.parse_args(args or [])


def run(args):
    """main function

    :param args: Command line parameters.
    """

    playlist = Playlist(args.playlist_url)

    delimiter = args.delimiter
    for v in paginate(playlist):
        index = v['index']['simpleText']
        url = f"https://www.youtube.com/watch?v={v['videoId']}"
        title = v['title']['runs'][0]['text']
        length = v['lengthText']['simpleText']
        print(delimiter.join((index, url, title, length)))


def main(args=sys.argv[1:]):
    """main function

    :param args: Command line parameters.
    """
    sys.exit(run(parse_args(args)))


if __name__ == "__main__":
    main()
