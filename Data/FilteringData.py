from IPython.display import display
import webbrowser
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Loading the data from the csv for truck stops in Virginia
dftruck = pd.read_csv('VA Truck Stops.csv')

# filtering the data to only include the truck stops located off of I-81
dftruck = dftruck.loc[dftruck.Highway == 'I-81']

# Removes the decimal place that is part of the zip code
dftruck['ZIP'] = dftruck['ZIP'].astype(int)

# Makes the zipcode into a string so it can be used later in writing the full address of the truck stop
dftruck['ZIP'] = dftruck['ZIP'].astype(str)
# Making a csv file to hold all the data for the truck stops located off of I-81

# Adds a column that contains the full address of the truck stop
dftruck['full_address'] = dftruck.Street_Address + ',' + \
    dftruck.City + ',' + dftruck.State + ',' + dftruck.ZIP

# Removes the qutation marks that the full address has
dftruck['full_address'] = dftruck.full_address.replace('""', '')

# sets up the geolocator so it can be used to read the addresses of the truck stops and coverts them to gps coordinates
geolocator = Nominatim(user_agent="Python")

# Empty lists for the latitude and longitude coordinates of each address
lat = []
long = []

# This function loops through the truck stops addresses and checks if the address has a GPS coordinate, if a GPS coordinate is not found
# it returns None for the latitude and longitude, if it is found it returns the latitude and longitude
for row in dftruck['full_address']:
    location = geolocator.geocode(row)
    if location is None:
        latitude = None
        longitude = None
    else:
        latitude = location.latitude
        longitude = location.longitude
    lat.append(latitude)
    long.append(longitude)

# adds a longitude and latitude column to the data frame
dftruck['latitude'] = lat
dftruck['longitude'] = long

alltruckstops = pd.read_csv('Truck_Stop_Points.csv')
map = folium.Map(location=[37.806507, -
                 79.389342], zoom_start=8)
for index, row in alltruckstops.iterrows():
    folium.Marker(location=(row['latitude'], row['longitude'])).add_to(map)

map.save('map1.html')
webbrowser.open('map1.html')
