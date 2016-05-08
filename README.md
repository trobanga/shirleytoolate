# shirleytoolate
The ultimate and nothing less than the bestest!



For testing purpose, create a calendar with radicale:
```python
import caldav
cli = caldav.DAVClient('http://localhost:5232/trobanga/cal1/')
p = cli.principal()
p.make_calendar(name="test", cal_id="cal1/")

# check if it was created
p.calendars()

# to add an event
vcal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:1234567890
DTSTAMP:20100510T182145Z
DTSTART:20100512T170000Z
DTEND:20100512T180000Z
SUMMARY:This is an event
END:VEVENT
END:VCALENDAR
"""
c = p.calendars([0])
c.add_event(vcal)
```
