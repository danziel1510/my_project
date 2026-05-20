import re

import streamlit as st
from back import Location
import json
import os
import datetime
import re

file_name = f"data {datetime.datetime.now().strftime('%Y-%m-%d')}.json"
st.set_page_config(
    page_title="Smart Attendance System",
    page_icon="✍",
    layout='wide',
    initial_sidebar_state="expanded",
)

st.write("Welcome to your attendance system")
col1, col2, col3 = st.columns(3)

with col1:
    first_name = st.text_input("First Name")
 
with col2:
    last_name = st.text_input("Last Name")

with col3:
    matric_number = st.text_input("Enter your matric number",
    placeholder="e.g 22/ENG05/009",).upper()

pattern = r"^\d{2}/[A-Z]{3}\d{2}/\d{3}$"
if matric_number and not re.match(pattern, matric_number):
    st.warning("Please enter a valid matric number in the format: 22/ENG05/009")

#st.write(first_name, last_name, matric_number)
location = Location()
status = location.state()
attendance = []
attendance.append([first_name, last_name, matric_number])
if  first_name == "" or last_name == "" or matric_number == "":
    st.warning("Please fill in all fields to submit attendance.")

record = {
    "first_name": first_name,
    "last_name": last_name,
    "matric_number": matric_number
}

def save_attendance(record):
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if st.button("Submit Attendance"):
    if status is True:
        if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
            with open(file_name, "r", encoding="utf-8") as f:
                attendance = json.load(f)
        if record not in attendance:
            save_attendance(record)
            st.success("Attendance submitted successfully.")
        else:
            st.warning("Attendance already submitted.")
    elif status is False:
        st.error("Attendance Rejected: You are not within the allowed radius.")
    else:
        st.warning("Please allow location access in your browser.")

