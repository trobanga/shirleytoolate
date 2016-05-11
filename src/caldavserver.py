#!/usr/bin/python3

import sanity_check
import caldav
import logging
import config


class CalDAVserver():
    """
    Interface to calendar server using caldav.
    """
    def __init__(self, url):
        self.url = url
        self.client = caldav.DAVClient(url)
        logging.debug('client: {}'.format(self.client))
        self.principal = self.client.principal()
        logging.debug('principal: {}'.format(self.principal))
        self.calendars = self.principal.calendars()
        logging.debug('calendars: {}'.format(self.calendars))

        # get calendar IDs
        props = [c.get_properties([caldav.elements.dav.Href(),
                                   caldav.elements.dav.DisplayName()])
                             for c in self.calendars]
        self.calendar_IDs = [p['{DAV:}href'] for p in props]
        self.calendar_DisplayNames = [p['{DAV:}displayname'] for p in props]
            
        
    def create_calendar(self, name, cal_id):
        """
        Create a new calendar on this server.
        name: Displayname of calendar
        cal_id: unique ID
        """
        cal_id = sanity_check.trailing_slash(cal_id)
        if any([i.endswith(cal_id) for i in self.calendar_IDs]):
            raise Exception("ID {} already exists in url {}.".format(cal_id, self.url))
        if name in self.calendar_DisplayNames:
            raise Exception("Calendar name {} already exists in url {}.".format(name, self.url))
        try:
            self.principal.make_calendar(name=name, cal_id=cal_id)
            logging.info("Created new calendar {}, {}".format(name, cal_id))
            self.calendars = self.principal.calendars()
            logging.debug('calendars: {}'.format(self.calendars))
            self.calendar_IDs.append(cal_id)
        except Exception as e:
            print(e)
            logging.info("Creation of new calendar {}, {} failed".format(name, cal_id))



    def delete_calendar(self, cal_id):
        """
        Delete calendar with ID cal_id.
        """
        cal_id = sanity_check.trailing_slash(cal_id)
        try:
            for c in self.calendars:
                if c.get_properties([caldav.elements.dav.Href()])['{DAV:}href'].endswith(cal_id):
                    c.delete()
                    logging.info("Deleted calendar with ID {}".format(cal_id))
                    return
            raise Exception("Calendar with ID {} does not exist.".format(cal_id))
        except Exception as e:
            print(e)
