#!/usr/bin/env python3

import config
import logging
import sanity_check
import caldavserver
import show_command


#def show(c, args):
#    if args.events:
#        for e in c.events():
#            show_command.event_print(e.data)
#        #print(list(map(show_command.event_print,c.events() )))
#
#
#
#=======
servers = {}
calendars  = []

def show(*args):
    """
    Handler for show cmd option.
    """

    args = vars(args[0])

    if args["calendars"]:
        for k,v in servers.items():
            print('Server nick: {}'.format(k))
            print("Calendars:")
            for cal in v.calendars:
                print(cal)

    elif args["events"]:
        for e in show_command.event_list(calendars):
            show_command.event_print(e)

def create(*args):
    """
    Handler for create cmd option
    """
    args = vars(args[0])
    if "calendar" in args:
        url_nick = args['calendar'][0]
        cal_name = args['calendar'][1]
        cal_id = args['calendar'][2]
        if url_nick in servers:
            servers[url_nick].create_calendar(cal_name, cal_id)
        

        
if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser('shirleytoolate')
    parser.add_argument('--debug', '-d', action='store_true', help='verbose logging')

    subparser = parser.add_subparsers()
    parser_show = subparser.add_parser("show", help='Show calendars, events, etc.')
    parser_show.add_argument("--events", nargs='+', help="show events")
    parser_show.add_argument("--url", action='store_true', help="show url of calendar")
    parser_show.add_argument("--calendars", action='store_true', help="show calendars")
    parser_show.set_defaults(func=show)

    parser_create = subparser.add_parser("create", help="Create calendars, events, etc.")
    parser_create.add_argument("--calendar", nargs=3,
                               metavar=('URL_nick', 'calendar_name', 'cal_id'),
                               help="create a new calendar ")
    parser_create.set_defaults(func=create)

    args = parser.parse_args()


    if args.debug:
        logging.basicConfig(filename='shirleys.log',level=logging.DEBUG)
    else:
        logging.basicConfig(filename='shirleys.log',level=logging.INFO)


    config.url = {k: sanity_check.trailing_slash(v) for k,v in config.url.items()}

    for k, v in config.url.items():
        servers[k] = caldavserver.CalDAVserver(v)
        for k,v in servers.items():
            for c in v.calendars:
                calendars.append(c)

            
    args.func(args)
