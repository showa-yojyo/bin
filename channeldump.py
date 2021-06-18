#!/usr/bin/env python

"""
A YouTube channel simple viewer

Usage: See channedumpl.py --help

Example:
bash$ channeldump.py https://www.youtube.com/channel/UCPrifqgoJmq7UgmRkZUKTJQ
"""

from argparse import ArgumentParser
import sys
from pytube import Channel
from pytubemod import paginate

__version__ = '1.0.0'

def extract_videos(initial_data):
    """A modified Channel._extract_videos

    :param initial_data: Input json extracted from the page or the last
        server response
    :returns: Tuple containing a list of up to 100 video data and
        a continuation token, if more videos are available
    """

    try:
        videos = initial_data["contents"][
            "twoColumnBrowseResultsRenderer"][
            "tabs"][1]["tabRenderer"]["content"][
            "sectionListRenderer"]["contents"][0][
            "itemSectionRenderer"]["contents"][0][
            "gridRenderer"]["items"]
    except (KeyError, IndexError, TypeError):
        try:
            # this is the json tree structure, if the json was directly sent
            # by the server in a continuation response
            important_content = initial_data[1]['response']['onResponseReceivedActions'][
                0
            ]['appendContinuationItemsAction']['continuationItems']
            videos = important_content
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

    return ([i['gridVideoRenderer'] for i in videos], continuation)


def parse_args(args):
    """Parse the command line parameters.

    Most options are taken from GNU wget.

    :param args: Raw command line arguments.
    :rtype: argparse.Namespace
    """

    parser = ArgumentParser(
        description='A YouTube channel simple viewer',
        epilog='Mail bug reports and suggestions to <yojyo@hotmail.com>',
        add_help=False)

    parser.add_argument(
        'channel_url',
        metavar='URL',
        help='URL of a channel')

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

    channel = Channel(args.channel_url)
    delimiter = args.delimiter
    for v in paginate(channel, extract_videos):
        url = f"https://www.youtube.com/watch?v={v['videoId']}"
        title = v['title']['runs'][0]['text']
        pubdate = v['publishedTimeText']['simpleText']
        count = v['viewCountText']['simpleText']
        print(delimiter.join((url, title, pubdate, count)))


def main(args=sys.argv[1:]):
    """main function

    :param args: Command line parameters.
    """
    sys.exit(run(parse_args(args)))


if __name__ == "__main__":
    main()
