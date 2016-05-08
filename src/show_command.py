##################################################
### show routines and pretty printing
##################################################

from icalendar import Calendar

def event_print(calstring):
   parsed_cal = Calendar.from_ical(calstring)
   print(50*'-')
   print ( parsed_cal.subcomponents)


