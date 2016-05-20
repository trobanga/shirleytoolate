#!/usr/bin/env python3

import logging
import sanity_check
import caldavserver
import show_command
import tui

import cursed

servers = {}

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
        if args['events'][0] == 'all':
            for k,v in servers.items():
                for d in v.calendars:
                    for e in v.get_events(d):
                        show_command.event_print(d,e)
        else:
            try:
                for a in args['events']:
                    v = servers[a]
                    for d in v.calendars:
                        for e in v.get_events(d):
                            show_command.event_print(d,e)
            except Exception as e:
                print("Calendar server {} not known.".format(e))
    elif args["url"]:
        for k,v in servers.items():
            print("{}: {}".format(k, v.url))


                
def add(*args):
    """
    Handler for create cmd option
    """
    args = vars(args[0])
    if args["calendar"]:
        url_nick = args['calendar'][0]
        cal_name = args['calendar'][1]
        cal_id = args['calendar'][2]
        if url_nick in servers:
            servers[url_nick].create_calendar(cal_name, cal_id)
        else:
            raise Exception("URL nick not known")

    elif args["event"]:
        print(calendars)
        print(args['event'][0])
        if args['event'][0] in get_calendars():
            print("start curse")
            e = cursed.run()
            print(e)

            
def delete(*args):
    """
    Handler to delete things.
    """
    args = vars(args[0])
    if args["calendar"]:
        url_nick = args['calendar'][0]
        cal_id = args['calendar'][1]
        if url_nick in servers:
            servers[url_nick].delete_calendar(cal_id)
        else:
            raise Exception("URL nick not known")

        
def start_tui(*args):
    """
    Starts the curses based terminal interface
    """
    args = vars(args[0])
    tui.start_tui(args)


def get_urls(url_conf="url.conf"):
    """
    Return dictionary with url_nick & url listed in url_conf
    """
    u = {}
    with open(url_conf, 'r') as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            if l.strip()[0] != '#':
                l = l.split(' ')
                if len(l) != 2:
                    continue
                l[1] = sanity_check.trailing_slash(l[1].rstrip())
                u[l[0]] = l[1]
    return u
                


def get_calendars():
    """
    Returns a list of all available calendars.
    """
    import itertools
    return itertools.chain(*[c.calendars for c in servers.values()])


def init_servers(urls):
    """
    Initializes and returns servers given in url (dictionary with url_nick & url).
    """
    return {k: caldavserver.CalDAVserver(k, v) for k, v in urls.items()}

                
if __name__ == "__main__":
    import sys
    import argparse


    
    parser = argparse.ArgumentParser('shirley (toolate)')
    parser.add_argument('--debug', '-d', action='store_true', help='verbose logging')

    subparser = parser.add_subparsers()
    parser_show = subparser.add_parser("shows", help='Show calendars, events, etc.')
    parser_show.add_argument("--events", nargs='+', help="show events")
    parser_show.add_argument("--url", action='store_true', help="show url of calendar")
    parser_show.add_argument("--calendars", action='store_true', help="show calendars")
    parser_show.set_defaults(func=show)

    parser_add = subparser.add_parser("adds", help="Add calendars, etc.")
    parser_add.add_argument("--calendar", nargs=3,
                               metavar=('URL_nick', 'calendar_name', 'cal_id'),
                               help="add a new calendar ")
    parser_add.add_argument("--event", nargs=1,
                            metavar=("calendar_name"),
                            help="add a new event to calendar")
    parser_add.set_defaults(func=add)

    parser_del = subparser.add_parser("del", help="Delete calendars, etc.")
    parser_del.add_argument("--calendar", nargs=2,
                            metavar=("URL nick, cal_id"),
                            help="Delete calendar from URL.")
    parser_del.set_defaults(func=delete)
    
    parser_del = subparser.add_parser("curses", help="Start textual user interface")
    parser_del.set_defaults(func=start_tui)

    args = parser.parse_args()


    if args.debug:
        logging.basicConfig(filename='shirleys.log',level=logging.DEBUG)
    else:
        logging.basicConfig(filename='shirleys.log',level=logging.INFO)

    
    servers = init_servers(get_urls())
     
    if args:       
        args.func(args)
