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
        cal_id = sanity_check.sanity_check(cal_id)
        self.principal.make_calendar(name=name, cal_id=cal_id)
