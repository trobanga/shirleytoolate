import urwid

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

def start_tui(args):
    txt = urwid.Text(u"Hello World")
    fill = urwid.Filler(txt, "top")
    loop =urwid.MainLoop(fill, unhandled_input=exit_on_q)
    loop.run()
