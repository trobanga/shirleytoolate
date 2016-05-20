##################################################
### show routines and pretty printing
##################################################

import icalendar 

def event_list(calendars, *conditions):
    e_list = []
    for c in calendars:
        for e in c['calendar'].events():
            if all(conditions):
                e_list.append((c['displayname'], e))
    return e_list


def event_print(displayname, event):
    events = icalendar.Calendar.from_ical(event.data).subcomponents
    for e in events:
        print("{}".format(displayname))
        print("   {}".format(e['SUMMARY']))

        start = ''
        end = ''
        if "DTSTART" in e:
            start = tformat(e['DTSTART'])
        if "DTEND" in e:
            end = tformat(e['DTEND'])
        print("   {} - {}".format(start, end))
        print(50*'-')

        
def tformat(tprop):
    return tprop.dt.ctime()
    
    



