from icalendar import Calendar
from dateutil.rrule import rrulestr
from datetime import datetime, timedelta, time, date
from zoneinfo import ZoneInfo
import requests
from calendarData import ics_list

def getEvents(ics_url, start_range, end_range, calendar_name=None):
    events = []
    
    r = requests.get(ics_url)
    cal = Calendar.from_ical(r.content)

    for component in cal.walk():
        if component.name == "VEVENT":
            dtstart = component.get("DTSTART").dt
            dtend = component.get("DTEND").dt
            summary = component.get("SUMMARY")

            if isinstance(dtstart, date) and not isinstance(dtstart, datetime):
                dtstart = datetime.combine(dtstart, time.min)
            if isinstance(dtend, date) and not isinstance(dtend, datetime):
                dtend = datetime.combine(dtend, time.min)

            # Normalize naive datetimes
            if dtstart.tzinfo is None:
                dtstart = dtstart.astimezone(ZoneInfo("Asia/Manila"))
            if dtend.tzinfo is None:
                dtend = dtend.astimezone(ZoneInfo("Asia/Manila"))

            rrule_data = component.get("RRULE")

            # RECURRING EVENT
            if rrule_data:
                rule = rrulestr(
                    str(rrule_data.to_ical().decode()),
                    dtstart=dtstart
                )
                for occur in rule.between(start_range, end_range, inc=True):
                    duration = dtend - dtstart
                    occur_end = occur + duration

                    occur = occur.astimezone(ZoneInfo("Asia/Manila"))
                    occur_end = occur_end.astimezone(ZoneInfo("Asia/Manila"))

                    events.append({
                        "start": occur,
                        "end": occur_end,
                        "summary": summary,
                        "calendar": calendar_name
                    })
            else:
                # ONE-TIME EVENT
                if start_range <= dtstart <= end_range:
                    dtstart = dtstart.astimezone(ZoneInfo("Asia/Manila"))
                    dtend = dtend.astimezone(ZoneInfo("Asia/Manila"))

                    events.append({
                        "start": dtstart,
                        "end": dtend,
                        "summary": summary,
                        "calendar": calendar_name
                    })
    print(f"Loaded {len(events)} events from {calendar_name}")
    return events
