from streamlit_geolocation import streamlit_geolocation
from geopy.distance import geodesic

class Location:
    OFFICE_LATITUDE = 9.103837578197247
    OFFICE_LONGITUDE = 7.410951638575079
    ALLOWED_RADIUS = 10000

    def user_location(self):
        location = streamlit_geolocation()
        if not location:
            return None
        return (location["latitude"], location["longitude"])

    def office_location(self):
        return (self.OFFICE_LATITUDE, self.OFFICE_LONGITUDE)

    def distance(self):
        user_coords = self.user_location()
        if not user_coords:
            return None
        return geodesic(self.office_location(), user_coords).meters

    def state(self):
        distance = self.distance()
        if distance is None:
            return None
        return distance <= self.ALLOWED_RADIUS