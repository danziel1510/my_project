import re
import datetime
import streamlit as st
from back import Location
from storage import AttendanceStorage

st.set_page_config(
    page_title="Smart Attendance System",
    page_icon="✍",
    layout="wide",
    initial_sidebar_state="expanded",
)

storage = AttendanceStorage()

st.write("Welcome to your attendance system")
if storage.use_sheets:
    st.info("Attendance is being saved to Google Sheets.")
else:
    st.info("Running in local fallback mode. Add Streamlit secrets for Google Sheets storage.")

col1, col2, col3 = st.columns(3)

with col1:
    first_name = st.text_input("First Name")

with col2:
    last_name = st.text_input("Last Name")

with col3:
    matric_number = st.text_input(
        "Enter your matric number",
        placeholder="e.g 22/ENG05/009",
    ).upper()

pattern = r"^\d{2}/[A-Z]{3}\d{2}/\d{3}$"
if matric_number and not re.match(pattern, matric_number):
    st.warning("Please enter a valid matric number in the format: 22/ENG05/009")

location = Location()
status = location.state()

if st.button("Submit Attendance"):
    if not first_name or not last_name or not matric_number:
        st.warning("Please fill in all fields to submit attendance.")
    elif status is False:
        st.error("Attendance Rejected: You are not within the allowed radius.")
    elif status is None:
        st.warning("Please allow location access in your browser.")
    else:
        record = {
            "first_name": first_name,
            "last_name": last_name,
            "matric_number": matric_number,
        }
        if storage.has_duplicate(record):
            st.warning("Attendance already submitted.")
        else:
            storage.save_attendance(record)
            st.success("Attendance submitted successfully.")

