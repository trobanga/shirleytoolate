#!/usr/bin/env python3

# cli = caldav.DAVClient('http://trobanga:wurst@localhost:5232/trobanga/cal/')
# p = cli.principal()
# c = p.calendar()
# e = c.add_event(vcal)

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
    
    
    server = caldavserver.CalDAVserver(config.url)

    for c in server.calendars:
        print(c.name)
    
    # calendar.show(args)
    
#    subargs = subparser.parse_args()

    args.func(calendar, args)



    
