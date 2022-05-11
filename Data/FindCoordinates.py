import pandas as pd
from geopy.geocoders import Nominatim


# Loading the data from the csv for truck stops in Virginia
dftruck = pd.read_csv('VA Truck Stops.csv')

# filtering the data to only include the truck stops located off of I-81
dftruck = dftruck[dftruck['Highway'].str.contains("81")]

# Removes the decimal place that is part of the zip code
dftruck['ZIP'] = dftruck['ZIP'].astype(int)

# Makes the zipcode into a string so it can be used later in writing the full address of the truck stop
dftruck['ZIP'] = dftruck['ZIP'].astype(str)


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

# This was used to save the filtered data as a csv file, so the truck stops that didn't have latitude and longitude coordinates
# could be manually added to include them and then saved as a new filename (Updated_Truck_Stops.csv) for the Analysis 

# dftruck.to_csv('Known_Truck_Stops.csv', index=False)