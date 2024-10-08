from streamlit_calendar import calendar
import streamlit as st
calendar_options = {
    "editable": "true",
    "selectable": "true",
    "headerToolbar": {
        "left": "prev,next",
        "center": "title",
        "right": "timeGridDay",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": "timeGridDay",
    "resourceGroupField": "building",
    "resources": [
        {"id": "a", "building": "Building A", "title": "Building A"},
        {"id": "b", "building": "Building A", "title": "Building B"},
        {"id": "c", "building": "Building B", "title": "Building C"},
        {"id": "d", "building": "Building B", "title": "Building D"},
        {"id": "e", "building": "Building C", "title": "Building E"},
        {"id": "f", "building": "Building C", "title": "Building F"},
    ],
}
calendar_events = [
    {
        "title": "Event 1",
        "start": "2024-09-13T08:30:00",
        "end": "2024-09-13T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Event 2",
        "start": "2024-09-13T07:30:00",
        "end": "2024-09-13T10:30:00",
        "resourceId": "b",
    },
    {
        "title": "Event 3",
        "start": "2024-09-13T10:40:00",
        "end": "2024-09-13T12:30:00",
        "resourceId": "a",
    }
]
custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""

calendar = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)
st.write(calendar)