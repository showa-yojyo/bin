#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""twstream.py
"""

from secret import twitter_stream
from twitter.stream import Timeout, HeartbeatTimeout, Hangup
from pprint import pprint

__version__ = '1.0.0'

def main():
    # These arguments are optional:
    stream_args = dict(
        timeout=60,
        block=False,
        heartbeat_timeout=90)

    query_args = dict(
        language='ja',
        track='bot')

    csv_header = (
        'id',
        'created_at',
        'user[screen_name]',
        'user[name]',
        #'source',
        'text',)
    csv_format = '|'.join(('{' + i + '}' for i in csv_header))

    stream = twitter_stream(**stream_args)
    for tweet in stream.statuses.filter(**query_args):
        if not tweet:
            continue

        if tweet in (Timeout, HeartbeatTimeout, Hangup):
            print("{}".format(tweet))
            break

        if 'text' in tweet:
            #pprint(tweet)
            line = csv_format.format(**tweet)
            print(line.replace('\r', '').replace('\n', '\\n'))
            continue

        print("Unknown {}".format(tweet))

if __name__ == '__main__':
    main()
