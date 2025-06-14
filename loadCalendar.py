from collections import defaultdict
from calendarData import ics_list
from datetime import datetime, date, time
from zoneinfo import ZoneInfo
from getEvents import getEvents


# STEP 1: Load all events (wide date range to cover everything you care about)
all_events_by_calendar = defaultdict(list)

start_range = datetime(2025, 1, 1, tzinfo=ZoneInfo("Asia/Manila"))
end_range = datetime(2025, 12, 31, 23, 59, tzinfo=ZoneInfo("Asia/Manila"))

for cal in ics_list:
    events = getEvents(cal["url"], start_range, end_range, calendar_name=cal["name"])
    all_events_by_calendar[cal["name"]] = events

print("Loaded all calendar events into memory.")
