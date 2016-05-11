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
        props = [c.get_properties([caldav.elements.dav.DisplayName()]) for c in calendars]
        cal_displaynames = [p['{DAV:}displayname'] for p in props]
        self.calendars = dict(zip(cal_displaynames, calendars))
        logging.debug('CalDAVserver.__init__.calendars: {}'.format(self.calendars))

        
               
    def create_calendar(self, displayname, cal_id):
        """
        Create a new calendar on this server.
        name: Displayname of calendar
        cal_id: unique ID
        """

        if displayname in self.calendars:
            raise Exception("CalDAVserver.create_calendar: Calendar name {} already exists in url {}.".format(name, self.url))

        # check if cal_id exists
        cal_id = sanity_check.trailing_slash(cal_id)
        calendars = self.principal.calendars()        
        props = [c.get_properties([caldav.elements.dav.Href()]) for c in calendars]
        cal_ids = [p['{DAV:}href'] for p in props]
        if any([i.endswith(cal_id) for i in cal_ids]):
            raise Exception("CalDAVserver.create_calendar: ID {} already exists in url {}.".format(cal_id, self.url))
        
        try:
            new_calendar = self.principal.make_calendar(name=displayname, cal_id=cal_id)
            logging.info("Created new calendar {}, {}".format(displayname, cal_id))
            self.calendars[displayname] = new_calendar
            logging.debug('CalDAVserver.create_calendar: current calendars: {}'.format(self.calendars))
            logging.info("Added new calendar {} with ID {} to url {}.".format(displayname, cal_id, self.url))
        except Exception as e:
            logging.debug(e)


    def delete_calendar(self, displayname):
        """
        Delete calendar with ID cal_id.
        """
        try:
            if displayname in self.calendars:
                self.calendars[displayname].delete()
                logging.info("Deleted calendar {} from url {}".format(displayname, self.url))
                del(self.calendars[displayname])
                return
            else:
                raise Exception("CalDAVserver.delete_calendar: Calendar {} does not exist in url.".format(displayname, self.url))
        except Exception as e:
            logging.debug("CalDAVserver.delete_calendar: Exception: {}".format(e))


    def add_event(self, e, displayname):
        """
        Add event e to calendar with ID cal_id.
        """
        if displayname in self.calendars:
            try:
                self.calendars[displayname].add_event(e)
            except Exception as e:
                logging.debug("CalDAVserver.add_event: Exception: {}".format(e))
            

    def get_events(self, displayname):
        """
        Returns a list of events of calendar displayname.
        """
        if displayname in self.calendars:
            return self.calendars[displayname].events()
        else:
            return []


    def get_all_events(self):
        """
        Returns iterator over all events on this server.
        """
        e = [v.events() for k, v in self.calendars.items()]
        import itertools
        e = itertools.chain(*e)
        return e
