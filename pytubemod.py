"""
pytubemod.py: module and modufication of pytube.Playlist._paginate
"""

import json
from pytube import request

def paginate(pl, extract_func):
    """A modified Playlist._paginate

    :param pl Playlist:
    :param extract_func func: TBW
    :returns: Iterable of YouTube video data
    """

    videos, continuation = extract_func(pl.initial_data)
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
        videos, continuation = extract_func(json.loads(req))
        yield from videos
        if continuation:
            load_more_url, headers, data = pl._build_continuation_url(continuation)
        else:
            load_more_url, headers, data = None, None, None
