from getEvents import getEvents
from calendarData import ics_list as calendar_list
from datetime import datetime, date, time
from zoneinfo import ZoneInfo
from collections import defaultdict
from loadCalendar import all_events_by_calendar
import streamlit as

def is_calendar_free(events, check_start, check_end):
    for e in events:
        # overlap check
        if e["start"] < check_end and e["end"] > check_start:
            return False
    return True

def main():
    # Step 1: Get input from user
    start_input = input("Enter start datetime (YYYY-MM-DD HH:MM): ")
    end_input = input("Enter end datetime (YYYY-MM-DD HH:MM): ")

    try:
        start_dt = datetime.strptime(start_input, "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("Asia/Manila"))
        end_dt = datetime.strptime(end_input, "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("Asia/Manila"))
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD HH:MM.")
        return

    # Step 2: Check calendars
    free_calendar_names = [
    name for name, events in all_events_by_calendar.items()
    if is_calendar_free(events, start_dt, end_dt)
    ]

    print("Free calendars in that timeslot:")
    for name in free_calendar_names:
        print(name)

if __name__ == "__main__":
    main()
