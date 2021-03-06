#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
from twmods.commands.statuses import make_commands

DESCRIPTION = "A utility script to manage Twitter statuses."

USAGE = """
  twstatus.py [--version] [--help]
  twstatus.py statuses/mentions_timeline [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>] [--trim-user]
    [--contributor-details] [-E | --include-entities]
  twstatus.py statuses/user_timeline [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>] [--trim-user]
    [-X | --exclude-replies] [--contributor-details] [--include-rts]
    <userspec>
  twstatus.py statuses/home_timeline [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>] [--trim-user]
    [-X | --exclude-replies] [--contributor-details] [--include-rts]
  twstatus.py statuses/retweets_of_me [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>] [--trim-user]
    [-E | --include-entities] [--include-user-entities]
  twstatus.py statuses/retweets/:id [-c | --count <n>]
    [--trim-user] <status_id>
  twstatus.py statuses/show/:id [--trim-user] [--include-my-retweet]
    [-E | --include-entities] <status_id>
  twstatus.py statuses/destroy/:id [--trim-user] <status_id>
  twstatus.py statuses/update [--in-reply-to-status-id <status_id>]
    [--possibly-sensitive] [--lat <Y>] [--long <X>]
    [--place-id <place>] [--display-coordinates] [--trim-user]
    [--media-ids <media_id>] <text>
  twstatus.py statuses/retweet/:id  [--trim-user] <status_id>
  twstatus.py statuses/unretweet/:id  [--trim-user] <status_id>
  twstatus.py statuses/oembed [--max-width <n>] [--hide-media]
    [--hide-thread] [--omit-script] [--omit-script]
    [--align {none,center,left,right}] [--related <csv-of-screen-names>]
    [--lang <lang>] [--widget-type {video}] [--hide-tweet]
    <status_id | url>
  twstatus.py statuses/retweeters/ids [--cursor <n>] [--stringify-ids]
    <status_id>
  twstatus.py statuses/lookup [-E | --include-entities] [--trim-user]
    [--map] <csv_of_status_ids>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.1.0'

MANAGER = make_manager(make_commands, globals())(__file__)

if __name__ == '__main__':
    MANAGER.main()
