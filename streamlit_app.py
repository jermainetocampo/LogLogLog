import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from getEvents import getEvents
from calendarData import ics_list

@st.cache_data
def load_all_events(start_range, end_range):
    all_events = []
    for calendar in ics_list:
        events = getEvents(calendar["url"], start_range, end_range, calendar_name=calendar["name"])
        all_events.extend(events)
    return all_events

st.title("Check Free Calendars")

start_date = st.date_input("Start date")
start_time = st.time_input("Start time")
end_date = st.date_input("End date")
end_time = st.time_input("End time")

if st.button("Check Availability"):
    start = datetime.combine(start_date, start_time).replace(tzinfo=ZoneInfo("Asia/Manila"))
    end = datetime.combine(end_date, end_time).replace(tzinfo=ZoneInfo("Asia/Manila"))

    preload_start = datetime(2025, 1, 1, tzinfo=ZoneInfo("Asia/Manila"))
    preload_end = datetime(2025, 6, 30, tzinfo=ZoneInfo("Asia/Manila"))
    all_events = load_all_events(preload_start, preload_end)

    busy = {e['calendar'] for e in all_events if start < e['end'] and end > e['start']}
    free = [cal["name"] for cal in ics_list if cal["name"] not in busy]

    st.write("✅ Free Calendars:" if free else "❌ No free calendars.")
    st.write(free)
