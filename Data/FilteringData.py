from IPython.display import display
import webbrowser
import pandas as pd
import folium
from geopy import distance
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

# Has all the points found in the above function and for every none type found, had to make edits to manually add the latitude and longitude
alltruckstops = pd.read_csv('Truck_Stop_Points.csv')

#Loading in data for the EV level 2 chargers
altlvl2 = pd.read_csv('alt_fuel_stations (Apr 25 2022).csv', usecols= ['EV Level2 EVSE Num', 'Latitude', 'Longitude'])

#Loading in data for the EV DC fast chargers 
altDC = pd.read_csv('alt_fuel_stations (Apr 25 2022).csv', usecols= ['EV DC Fast Count', 'Latitude', 'Longitude', 'Station Name'])


# Filtering the EV level 2 chargers so it only includes points closer to I-81 and drops the values that don't have a charger
altlvl2['EV Level2 EVSE Num'] = altlvl2['EV Level2 EVSE Num']
altlvl2 = altlvl2.dropna()
altlvl2['Longitude'] = altlvl2['Longitude'].astype(float)
df81lvl2 = altlvl2[altlvl2['Longitude'].between(-82.2, -78.1)]


# Filtering the EV DC fast chargers so it only includes points closer to I-81
altDC['EV DC Fast Count'] = altDC['EV DC Fast Count']
altDC['Longitude'] = altDC['Longitude'].astype(float)
df81DC = altDC[altDC['Longitude'].between(-82.2, -78.1)]

#Sorts the values from the bottom of I-81 to the top of I-81
df81DC = df81DC.sort_values(['Longitude'])


# Calculating distance between each point


alltruckstops['latitude'] = alltruckstops['latitude'].astype(float)
alltruckstops['longitude'] = alltruckstops['longitude'].astype(float)

df81DC['Latitude'] = df81DC['Latitude'].astype(float)
df81DC['Longitude'] = df81DC['Longitude'].astype(float)
df = pd.DataFrame()
dist = []
truckstop = []
evcharger = []
latit = []
longi = []
for idx, row in alltruckstops.iterrows():
    for index, rowdc in df81DC.iterrows():
        vectordist = distance.geodesic((row['latitude'], row['longitude']), (rowdc['Latitude'], rowdc['Longitude'])).mi
        dist.append(vectordist)
        truckstop.append(row['Exit'])
        evcharger.append(rowdc['Station Name'])
        latit.append(row['latitude'])
        longi.append(row['longitude'])
df = pd.DataFrame()
df['Exit'] = truckstop
df['Station_Name'] = evcharger
df['distance(mi)'] = dist
df['latitude'] = latit
df['longitude'] = longi


truckstopwithcharger = pd.DataFrame()
truck = []
closestcharger = []
mindist = []
for index, row in df.iterrows():
    if row['distance(mi)'] <= 1:
        truck.append(row['Exit'])
        closestcharger.append(row['Station_Name'])
        mindist.append(row['distance(mi)'])
    else:
        continue
truckstopwithcharger['Truck_Stop_Exit'] = truck
truckstopwithcharger['Charger'] = closestcharger
truckstopwithcharger['distancetocharger'] = mindist

nextstation = pd.DataFrame()
distancetstop = []
central = []
other = []
for idx, row in truckstopwithcharger.iterrows():
    for index, rowt in alltruckstops.iterrows():
        tstop = distance.geodesic((row['latitude'], row['longitude']), (rowt['latitude'], rowt['longitude'])).mi
        distancetstop.append(tstop)
        central.append(row['Exit'])
        other.append(rowt['Exit'])

nextstation['Tstop Charger'] = central
nextstation['Tstop Exit'] = other
nextstation['distance(mi)'] = distancetstop
print(nextstation)
# Creating the map and plotting all the GPS coordinates on the map
# map = folium.Map(location=[37.806507, -
#                  79.389342], zoom_start=8)
# for index, row in alltruckstops.iterrows():
#     folium.Marker(location=(row['latitude'], row['longitude'])).add_to(map)

# for index, row in df81lvl2.iterrows():
#     folium.Marker(location=(row['Latitude'], row['Longitude']),icon=folium.Icon(color='red')).add_to(map)

# for index, row in df81DC.iterrows():
#     folium.Marker(location=(row['Latitude'], row['Longitude']),icon=folium.Icon(color='orange')).add_to(map)


# map.save('map1.html')
# webbrowser.open('map1.html')

