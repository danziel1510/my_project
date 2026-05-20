import streamlit as st 
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from geopy.distance import geodesic

OFFICE_LATITUDE = 9.103837578197247
OFFICE_LONGITUDE = 7.410951638575079

ALLOWED_RADIUS = 200

location = streamlit_geolocation()

if location:
    user_lat = location["latitude"]
    user_lon = location["longitude"]

    st.success("Location received successfully.")

    st.write(f"Latitude: {user_lat}")
    st.write(f"Longitude: {user_lon}")


    office_coordinates = (OFFICE_LATITUDE, OFFICE_LONGITUDE)
    user_coordinates = (user_lat, user_lon)

    distance = geodesic(
        office_coordinates,
        user_coordinates
    ).meters

    st.write(f"Distance from office: {distance:.2f} meters")

    if distance <= ALLOWED_RADIUS:

        st.success("Attendance Accepted")

        if st.button("Submit Attendance"):

            # Save to database here later
            st.success("Attendance submitted successfully.")

    else:
        st.error("You are outside the approved location.")

else:
    st.warning("Please allow location access in your browser.")