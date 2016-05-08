#!/usr/bin/env python3

import config
import logging
import sanity_check
import caldavserver
import show_command


def show(c, args):
    if args.events:
        for e in c.events():
            show_command.event_print(e.data)
        #print(list(map(show_command.event_print,c.events() )))



if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser('shirleytoolate')
    parser.add_argument('--debug', '-d', action='store_true', help='more logging')

    subparser = parser.add_subparsers()
    parser_show = subparser.add_parser("show", help='show me your tits, Shirley!')
    parser_show.add_argument("--events", nargs='+', help="show events")
    parser_show.add_argument("--url", action='store_true', help="show url of calendar")
    parser_show.set_defaults(func=show)


    args = parser.parse_args()


    if args.debug:
        logging.basicConfig(filename='shirleys.log',level=logging.DEBUG)
    else:
        logging.basicConfig(filename='shirleys.log',level=logging.INFO)


    config.url = {sanity_check.sanity_check(k): list(map(sanity_check.sanity_check, v)) for k,v in config.url.items()}

    print(config.url)
    server = []
    for k, v in config.url.items():
        for c in v:
            server.append(caldavserver.CalDAVserver(k + c))

    print(50*'-')
    for s in server:
        for c in s.calendars:
            #print(c.name)
            args.func(c, args)
            

    # calendar.show(args)

    #subargs = subparser.parse_args()

