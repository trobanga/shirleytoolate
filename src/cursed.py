#!/usr/bin/env python3


import urwid

class EventWidget(urwid.Filler):
    def __init__(self, *args, **kwargs):
        
        self.start = urwid.Edit('Start: ')
        self.end = urwid.Edit('End: ')

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
        raise urwid.ExitMainLoop()
        
    # def mouse_event(self, size, event, button, col, row, focus):
    #     print(size, event, button, col, row, focus)


def run():

    top  = EventWidget(valign='top')    
    loop = urwid.MainLoop(top)
    loop.run()  
    
if __name__ == "__main__":
    run()

    
