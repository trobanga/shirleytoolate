#!/usr/bin/python3

import sanity_check
import caldav
import logging


class CalDAVserver():
    """
    Interface to calendars using caldav.
    """
    def __init__(self, url):
        self.client = caldav.DAVClient(url)
        logging.debug('client: {}'.format(self.client))
        self.principal = self.client.principal()
        logging.debug('principal: {}'.format(self.principal))
        self.calendars = self.principal.calendars()
        logging.debug('calendars: {}'.format(self.calendars))

    def create_calendar(self, name, cal_id):
        """
        Create a new calendar on this server.
        name: Displayname of calendar
        cal_id:
        """
        cal_id = sanity_check.trailing_slash(cal_id)
        try:
            self.principal.make_calendar(name=name, cal_id=cal_id)
            logging.info("Created new calendar {}, {}".format(name, cal_id))
            self.calendars = self.principal.calendars()
            logging.debug('calendars: {}'.format(self.calendars))
        except Exception as e:
            print(e)
            logging.info("Creation of new calendar {}, {} failed".format(name, cal_id))
