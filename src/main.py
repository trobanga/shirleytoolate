#!/usr/bin/env python3

import config
import logging
import sanity_check
import caldavserver


def show(c, args):
    if args.events and args.events[0] == 'all':
        c.show_events(args)



if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser('shirleytoolate')
    parser.add_argument('--debug', '-d', action='store_true', help='verbose logging')

    subparser = parser.add_subparsers()
    parser_show = subparser.add_parser("show", help='Show calendars, events, etc.')
    parser_show.add_argument("--events", nargs='+', help="show events")
    parser_show.add_argument("--url", action='store_true', help="show url of calendar")
    parser_show.set_defaults(func=show)

    parser_create = subparser.add_parser("create", help="Create calendars, events, etc.")
    parser_create.add_argument("--calendar", nargs=2, metavar=('URL_nick', 'calendar_name'), help="create a new calendar ")


    args = parser.parse_args()


    if args.debug:
        logging.basicConfig(filename='shirleys.log',level=logging.DEBUG)
    else:
        logging.basicConfig(filename='shirleys.log',level=logging.INFO)


    config.url = {k: (sanity_check.trailing_slash(v[0]),
                    list(map(sanity_check.trailing_slash, v[1])))
                    for k,v in config.url.items()}

    print(config.url)
    server = []
    for k, v in config.url.items():
        print("Server nick: {}".format(k))
        for c in v[1]:
            server.append(caldavserver.CalDAVserver(v[0] + c))

    for s in server:
        for c in s.calendars:
            print(c.name)

    # calendar.show(args)

#    subargs = subparser.parse_args()

#    args.func(calendar, args)
