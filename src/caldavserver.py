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

        self.calendars = [{}] # list with dict of calendar, cal_id, and displayname
        self.update_calendars()

        
    def update_calendars(self):
        """
        Update list of dict of calendar, cal_id, and displayname
        """
        calendars = self.principal.calendars()
        
        # get calendar IDs
        props = [c.get_properties([caldav.elements.dav.Href(),
                                   caldav.elements.dav.DisplayName()])
                             for c in calendars]
        cal_ids = [p['{DAV:}href'] for p in props]
        cal_displaynames = [p['{DAV:}displayname'] for p in props]

        self.calendars = [{"calendar": c,
                           "cal_id": cal_id,
                           "displayname": dn} for c, cal_id, dn in zip(calendars,
                                                                       cal_ids,
                                                                       cal_displaynames)]
        logging.debug('CalDAVserver.__init__.calendars: {}'.format(self.calendars))

               
    def create_calendar(self, displayname, cal_id):
        """
        Create a new calendar on this server.
        name: Displayname of calendar
        cal_id: unique ID
        """
        cal_id = sanity_check.trailing_slash(cal_id)
        if any([c['cal_id'].endswith(cal_id) for c in self.calendars]):
            raise Exception("CalDAVserver.create_calendar: ID {} already exists in url {}.".format(cal_id, self.url))
        if any([c['displayname'] == displayname for c in self.calendars]):
            raise Exception("CalDAVserver.create_calendar: Calendar name {} already exists in url {}.".format(name, self.url))
        try:
            new_calendar = self.principal.make_calendar(name=displayname, cal_id=cal_id)
            logging.info("Created new calendar {}, {}".format(displayname, cal_id))
            self.calendars.append({'calendar': new_calendar,
                                   'cal_id': cal_id,
                                   'displayname': displayname})
            logging.debug('CalDAVserver.create_calendar: current calendars: {}'.format(self.calendars))
            logging.info("Added new calendar {} with ID {} to url {}.".format(displayname, cal_id, self.url))
        except Exception as e:
            logging.debug(e)


    def delete_calendar(self, displayname):
        """
        Delete calendar with ID cal_id.
        """
        try:
            for c in self.calendars:
                if c['displayname'] == displayname:
                    c['calendar'].delete()
                    logging.info("Deleted calendar with ID {} from url {}".format(c['cal_id'], self.url))
                    self.update_calendars()
                    return
            raise Exception("CalDAVserver.delete_calendar: Calendar with ID {} does not exist in url.".format(c['cal_id'], self.url))
        except Exception as e:
            logging.debug("CalDAVserver.delete_calendar: Exception: {}".format(e))


    def add_event(self, e, displayname):
        """
        Add event e to calendar with ID cal_id.
        """
        for c in self.calendars:
            if c['displayname'] == displayname:
                try:
                    c.add_event(e)
                except Exception as e:
                    logging.debug("CalDAVserver.add_event: Exception: {}".format(e))
            

    def get_events(self, displayname):
        """
        Returns a list of events of calendar displayname.
        """
        for c in self.calendars:
            if c['displayname'] == displayname:
                return c.events()
                

                
