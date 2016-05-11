#!/usr/bin/python3

import sanity_check
import caldav
import logging
import config


class CalDAVserver():
    """
    Interface to calendar server using caldav.
    """
    def __init__(self, nick, url):
        self.url = url
        self.url_nick = nick
        self.client = caldav.DAVClient(url)
        logging.debug('CalDAVserver.__init__.client: {}'.format(self.client))
        self.principal = self.client.principal()
        logging.debug('CalDAVserver.__init__.principal: {}'.format(self.principal))
        self.calendars = self.principal.calendars()
        logging.debug('CalDAVserver.__init__.calendars: {}'.format(self.calendars))

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
            raise Exception("CalDAVserver.create_calendar: ID {} already exists in url {}.".format(cal_id, self.url))
        if name in self.calendar_DisplayNames:
            raise Exception("CalDAVserver.create_calendar: Calendar name {} already exists in url {}.".format(name, self.url))
        try:
            self.principal.make_calendar(name=name, cal_id=cal_id)
            logging.info("Created new calendar {}, {}".format(name, cal_id))
            self.calendars = self.principal.calendars()
            logging.debug('CalDAVserver.create_calendar: calendars: {}'.format(self.calendars))
            self.calendar_IDs.append(cal_id)
            logging.info("Added new calendar with ID {} to url {}.".format(cal_id, self.url))
        except Exception as e:
            logging.debug(e)



    def delete_calendar(self, cal_id):
        """
        Delete calendar with ID cal_id.
        """
        cal_id = sanity_check.trailing_slash(cal_id)
        try:
            for c in self.calendars:
                if c.get_properties([caldav.elements.dav.Href()])['{DAV:}href'].endswith(cal_id):
                    c.delete()
                    logging.info("Deleted calendar with ID {} from url {}".format(cal_id, self.url))
                    return
            raise Exception("CalDAVserver.delete_calendar: Calendar with ID {} does not exist in url.".format(cal_id, self.url))
        except Exception as e:
            logging.debug(e)
