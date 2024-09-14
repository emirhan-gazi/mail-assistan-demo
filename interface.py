from streamlit_calendar import calendar
import streamlit as st
import datetime
from server import extract


def interface():
    st.set_page_config(page_title="Mehmet Bey'in Takvimi", page_icon="📅")
    st.title("Mehmet Bey'in Takvimi")    
    
    def reset() -> None:
        st.session_state["events"] = []
        del st.session_state["events"]
    
    if "events" not in st.session_state:
        st.session_state["events"] = None

    st.info("Hoş geldiniz. Bu demoda Mehmet Bey' in asistanı olucaksınız. Mehmet Bey'in maillerini demoya girerek bir gün takvimini ayarlayın.", icon="ℹ️")


    today = datetime.date.today()

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
    st.session_state["events"] = [] if st.session_state["events"] is None else st.session_state["events"]

    


    col1, col2 = st.columns([1, 2])

    flag = True
    with col1:
        st.header("Mail Asistanı") 
        prompt = st.text_area(label = "Mail", height=400)


        if prompt:
            response = extract(prompt)
            day = response['day']
            if day == None : 
                day = today

            start = response['start']
            end = response['end']
            title = response['title']

           
            if start == None or end == None or title == None:
                flag = False
            
            st.session_state['events'].append({
                "title": title,
                "start": f"{day}T{start}",
                "end": f"{day}T{end}",
                "resourceId": "a",
            })


    with col2: 
        if flag == False:
            st.warning("Lütfen daha uygun mail giriniz.")
        else : 
            st.header("Takvim")
            calendar_event = calendar(events=st.session_state['events'], options=calendar_options, custom_css=custom_css)
            st.write(calendar_event)


    reset = st.button("Reset", on_click=reset)


if __name__ == "__main__":
    interface()


