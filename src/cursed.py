#!/usr/bin/env python3


import urwid
import caldavserver
import uuid
import logging
import icalendar
import datetime

class EventWidget(urwid.Filler):
    def __init__(self, *args, **kwargs):
        
        self.start = urwid.Edit('Start: ')
        self.end = urwid.Edit('End: ')

        self.server = kwargs["server"]
        self.calendar = kwargs["calendar"]

        del(kwargs['server'])
        del(kwargs["calendar"])

        print (self.server, self.calendar)

        
        div = urwid.Divider()
        self.msg = urwid.Edit(caption="Event message: ", edit_text='', multiline=True)
        button_save = urwid.Button('save')
        urwid.connect_signal(button_save, 'click', self.on_save)
        self.pile = urwid.Pile([self.start,
                                self.end,
                                div,
                                self.msg,
                                div,
                                button_save])

        super(EventWidget, self).__init__(self.pile, *args, **kwargs)

    def on_save(self, button):
        """
        Save and exit.
        """


        vcal = icalendar.Calendar()
        event = icalendar.Event()
        event['uid'] = self.calendar + str(uuid.uuid1())
        # event['dtstart'] = self._datetime_to_ical(datetime.datetime(2016,5,15))
        # event['dtend'] = self._datetime_to_ical(datetime.datetime(2016,5,15))
        event['summary'] = self.msg.edit_text
        vcal.add_component(event)       

        
        logging.debug("EventWidget:on_save:vcal: {}".format(vcal.to_ical()))
        r = self.server.add_event(vcal.to_ical(), self.calendar)
        logging.debug("EventWidget:on_save:add_event: {}".format(r))
        raise urwid.ExitMainLoop()


    def _datetime_to_ical(self, dt):
        """
        Converts datetime format to ical format and returns it.
        """
        return icalendar.vDatetime(dt).to_ical()

    
    
    def keypress(self, size, key):
        """
        Leave without saving, if pressing Esc.
        """
        if key == "esc":
            raise urwid.ExitMainLoop()
        super(EventWidget, self).keypress(size, key) 

        
def run(calendar, server):

    top  = EventWidget(valign='top', calendar=calendar, server=server)    
    loop = urwid.MainLoop(top)
    loop.run()  
    
if __name__ == "__main__":
    run()

    
